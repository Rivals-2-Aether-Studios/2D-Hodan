SteamParticle = Class( RivalsLua2DArticleEntity )

local LIFETIME = 25
local SCALE    = 2.5

local LifeTimer = nil

function SteamParticle:RegisterNetProps()
	LifeTimer = self:AddNetPropInt32()
end

function SteamParticle:InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )
	self:Super_InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )

	self:SetNetPropInt32( LifeTimer, 0 )
	self:SetSpriteOpacity( 1.0 )

	local key = Hodan2_Shared and Hodan2_Shared.NextSteamParticleKey
	if ( key ~= nil and key ~= "" ) then
		self:Set2DAnimation( key )
	end

	local dir = ( InFacing == ERivalsFacingDirection.Right ) and 1.0 or -1.0
	local vx  = -2.0 * SCALE * dir
	local vy  =  3.0 * SCALE
	self:SetVelocity( Vector2D:new( vx, vy ) )
end

function SteamParticle:ArticleUpdate()
	self:Super_ArticleUpdate()

	local t = self:GetNetPropInt32( LifeTimer ) + 1
	self:SetNetPropInt32( LifeTimer, t )

	if ( t >= LIFETIME ) then
		self:Deactivate()
		return
	end

	self:SetSpriteOpacity( 1.0 - ( t / LIFETIME ) )
end

function SteamParticle:GetActiveHitboxes( bIgnoreHitboxLocation ) return false end
