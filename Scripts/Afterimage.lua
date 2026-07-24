Afterimage = Class( RivalsLua2DArticleEntity )

local TRAIL_LIFETIME       = 7
local TRAIL_VISIBLE_FRAME  = 6
local DEFAULT_STATIC_LIFE  = 6

local Delay      = nil
local IsTrail    = nil
local Lifetime   = nil

function Afterimage:RegisterNetProps()
	Delay    = self:AddNetPropInt32()
	IsTrail  = self:AddNetPropBoolean()
	Lifetime = self:AddNetPropInt32()
end

function Afterimage:InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )
	self:Super_InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )

	self:SetNetPropInt32( Delay, 0 )

	self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )

	local key = Hodan2_Shared and Hodan2_Shared.NextAfterimageKey
	if ( key ~= nil and key ~= "" ) then
		self:Set2DAnimation( key )
	end

	local mode = Hodan2_Shared and Hodan2_Shared.NextAfterimageMode
	local is_trail = ( mode == nil or mode == "trail" )
	self:SetNetPropBoolean( IsTrail, is_trail )

	if ( is_trail ) then
		self:SetSpriteOpacity( 0.0 )
		self:SetNetPropInt32( Lifetime, TRAIL_LIFETIME )
	else
		self:SetSpriteOpacity( 1.0 )
		local life = ( Hodan2_Shared and Hodan2_Shared.NextAfterimageLifetime ) or 0
		if ( life <= 0 ) then life = DEFAULT_STATIC_LIFE end
		self:SetNetPropInt32( Lifetime, life )
	end
end

function Afterimage:ArticleUpdate()
	self:Super_ArticleUpdate()
	self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )

	local t = self:GetNetPropInt32( Delay ) + 1
	self:SetNetPropInt32( Delay, t )

	if ( self:GetNetPropBoolean( IsTrail ) ) then
		if ( t < TRAIL_VISIBLE_FRAME ) then return end
		if ( t == TRAIL_VISIBLE_FRAME ) then
			self:SetSpriteOpacity( 1.0 )
			return
		end
		self:Deactivate()
	else
		if ( t >= self:GetNetPropInt32( Lifetime ) ) then
			self:Deactivate()
		end
	end
end

function Afterimage:GetActiveHitboxes( bIgnoreHitboxLocation ) return false end
