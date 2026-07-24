Vapour = Class( RivalsLuaArticleEntity )

local SCALE = 2.5

local LifeTimer = nil
local Variant   = nil

local SPAWN_LEN = 40
local IDLE_LEN  = 420
local DIE_LEN   = 20
local IDLE_END  = SPAWN_LEN + IDLE_LEN
local TOTAL_END = SPAWN_LEN + IDLE_LEN + DIE_LEN
local IDLE_TICKS_PER_FRAME = 5
local IDLE_FRAME_COUNT     = 6
local IDLE_LOOP_LEN = IDLE_TICKS_PER_FRAME * IDLE_FRAME_COUNT

function Vapour:StartDying()
	local t = self:GetNetPropInt32( LifeTimer )
	if ( t < SPAWN_LEN + IDLE_LEN ) then
		self:SetNetPropInt32( LifeTimer, SPAWN_LEN + IDLE_LEN )
	end
end

function Vapour:IsDying()
	return self:GetNetPropInt32( LifeTimer ) >= SPAWN_LEN + IDLE_LEN
end

local function VariantKey( v )
	if ( v == 2 ) then return "vapour2"
	elseif ( v == 3 ) then return "vapour3"
	elseif ( v == 4 ) then return "vapour4"
	else return "vapour" end
end

function Vapour:RegisterNetProps()
	LifeTimer = self:AddNetPropInt32()
	Variant   = self:AddNetPropInt32( 1, 4 )
end

function Vapour:InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )
	self:Super_InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )
	self:SetNetPropInt32( LifeTimer, 0 )
	self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )

	local v
	if ( Hodan2_Shared and Hodan2_Shared.NextVapourIsParry ) then
		Hodan2_Shared.NextVapourIsParry = false
		v = 4
	else
		v = self:GetRandomIntRange( 1, 3 )
	end
	self:SetNetPropInt32( Variant, v )
	self:Set2DAnimation( VariantKey( v ) )
end

function Vapour:ArticleUpdate()
	self:Super_ArticleUpdate()
	self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )

	local t = self:GetNetPropInt32( LifeTimer ) + 1
	self:SetNetPropInt32( LifeTimer, t )

	if ( t >= TOTAL_END ) then
		self:Deactivate()
		return
	end

	local frame
	if ( t < SPAWN_LEN ) then
		frame = math.floor( t * 12 / SPAWN_LEN )
		if ( frame > 11 ) then frame = 11 end
	elseif ( t < IDLE_END ) then
		local loop_pos = ( t - SPAWN_LEN ) % IDLE_LOOP_LEN
		frame = 12 + math.floor( loop_pos / IDLE_TICKS_PER_FRAME )
	else
		frame = 18 + math.floor( ( t - IDLE_END ) * 3 / DIE_LEN )
		if ( frame > 20 ) then frame = 20 end
	end
	self:Lua_SetFlipbookFrame( frame )

	if ( t >= SPAWN_LEN and t < IDLE_END ) then
		local owner = self:GetOwnerRival()
		if ( owner ~= nil ) then
			local op = owner:GetLocation2D()
			local mp = self:GetLocation2D()
			local dx = op.X - mp.X
			local dy = op.Y - mp.Y
			if ( dx >= -66.0 * SCALE and dx <= 78.0 * SCALE
					and dy >= -90.0 * SCALE and dy <= 64.0 * SCALE ) then
				if ( Hodan2 and Hodan2.MaxSteamFromVapour ) then
					Hodan2.MaxSteamFromVapour( owner )
				end
			end
		end
	end
end
