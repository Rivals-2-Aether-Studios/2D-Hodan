SteamParticle = Class( RivalsLua2DArticleEntity )

local LIFETIME   = 25
local MAX_FRAMES = 25
local SCALE      = 2.5

local LifeTimer = nil
local Align     = nil
local SteamDir  = nil
local BothMaxed = nil

local function EaseExpoIn( a, b, t, dur )
	return a + ( b - a ) * ( 2.0 ^ ( 10.0 * ( t / dur ) - 10.0 ) )
end

function SteamParticle:RegisterNetProps()
	LifeTimer = self:AddNetPropInt32()
	Align     = self:AddNetPropInt32( 0, 1 )
	SteamDir  = self:AddNetPropInt32( -1, 1 )
	BothMaxed = self:AddNetPropBoolean()
end

function SteamParticle:InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )
	self:Super_InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )

	self:SetNetPropInt32( LifeTimer, 0 )
	self:SetSpriteOpacity( 1.0 )

	local key = Hodan2_Shared and Hodan2_Shared.NextSteamParticleKey
	if ( key ~= nil and key ~= "" ) then
		self:Set2DAnimation( key )
	end
	self:SetNetPropInt32( Align, ( Hodan2_Shared.NextSteamAlign == "v" ) and 1 or 0 )
	self:SetNetPropInt32( SteamDir, ( tonumber( Hodan2_Shared.NextSteamDir ) or 1 ) >= 0 and 1 or -1 )
	self:SetNetPropBoolean( BothMaxed, Hodan2_Shared.NextSteamBothMaxed and true or false )

	self:Lua_SetFlipbookFrame( 0 )
	self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )
end

function SteamParticle:ArticleUpdate()
	self:Super_ArticleUpdate()

	local t = self:GetNetPropInt32( LifeTimer )

	local dir = self:GetNetPropInt32( SteamDir )
	local hsp, vsp = 0.0, 0.0
	if ( self:GetNetPropBoolean( BothMaxed ) ) then
		hsp = EaseExpoIn( 2.0, 9.0, t, LIFETIME ) * -dir
		vsp = EaseExpoIn( 4.0, 9.0, t, LIFETIME )
	elseif ( self:GetNetPropInt32( Align ) == 0 ) then
		hsp = EaseExpoIn( 2.0, 9.0, t, LIFETIME ) * -dir
		vsp = EaseExpoIn( 1.0, 3.0, t, LIFETIME )
	else
		vsp = EaseExpoIn( 4.0, 9.0, t, LIFETIME )
	end
	self:SetVelocity( Vector2D:new( hsp * SCALE, vsp * SCALE ) )

	t = t + 1
	self:SetNetPropInt32( LifeTimer, t )

	if ( t >= LIFETIME ) then
		self:Deactivate()
		return
	end

	local frame = t - 1
	if ( frame < 0 ) then frame = 0 end
	if ( frame > MAX_FRAMES - 1 ) then frame = MAX_FRAMES - 1 end
	self:Lua_SetFlipbookFrame( frame )
end

function SteamParticle:GetActiveHitboxes( bIgnoreHitboxLocation ) return false end
