Sweatwhirl = Class( RivalsLuaArticleEntity )

local function GetVapourAD()
	Hodan2_Shared.VapourAD = Hodan2_Shared.VapourAD
		or LoadArticleData( "/Game/ModContent/3752556104/UnrealAssets/Articles/AD_Hodan2_Vapour" )
		or LoadArticleData( "/Game/ModContent/3752556104/PublishedAssets/Articles/AD_Hodan2_Vapour" )
	return Hodan2_Shared.VapourAD
end

local SCALE = 2.5

local IsFast    = nil
local LifeTimer = nil
local Level     = nil
local LastSprite = nil
local HitCount  = nil
local Bashed    = nil
local Caught    = nil
local Thrown    = nil

function Sweatwhirl:RegisterNetProps()
	IsFast     = self:AddNetPropBoolean()
	LifeTimer  = self:AddNetPropInt32()
	Level      = self:AddNetPropInt32()
	LastSprite = self:AddNetPropInt32()
	HitCount   = self:AddNetPropInt32()
	Bashed     = self:AddNetPropBoolean()
	Caught     = self:AddNetPropBoolean()
	Thrown     = self:AddNetPropBoolean()
end

function Sweatwhirl:MarkCaught()
	self:SetNetPropBoolean( Caught, true )
	self:SetWindowByName( "Held" )
	local lvl = self:GetNetPropInt32( Level )
	local key
	if     ( lvl >= 3 ) then key = "sweatwhirl_proj3_held"
	elseif ( lvl >= 2 ) then key = "sweatwhirl_proj2_held"
	else                     key = "sweatwhirl_proj_held"  end
	self:Set2DAnimation( key )
	self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )
end

function Sweatwhirl:DropWithVapor()
	self:SetNetPropBoolean( Caught, false )
	self:Deactivate()
end

function Sweatwhirl:ReleaseToThrow( vx, vy, is_spike_throw )
	self:SetNetPropBoolean( Caught, false )
	self:SetNetPropBoolean( Thrown, is_spike_throw and true or false )
	self:SetWindowByName( "Travel" )
	local lvl = self:GetNetPropInt32( Level )
	local key
	if     ( lvl >= 3 ) then key = "sweatwhirl_proj3"
	elseif ( lvl >= 2 ) then key = "sweatwhirl_proj2"
	else                     key = "sweatwhirl_proj"  end
	self:Set2DAnimation( key )
	self:SetNetPropInt32( LastSprite, lvl )
	self:SetVelocity( Vector2D:new( vx, vy ) )
end

function Sweatwhirl:GetCurrentLevel()
	return self:GetNetPropInt32( Level )
end

function Sweatwhirl:IsThrown()
	return self:GetNetPropBoolean( Thrown )
end

function Sweatwhirl:InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )
	self:Super_InitArticle( InArticleData, Creator, InLocation, InFacing, InitialWindowStringTableKey )

	local fast = Hodan2_Shared.ForceFast
	if ( not fast ) then
		local owner = self:GetOwnerRival()
		fast = ( owner ~= nil and owner:GetAttack() == ERivalsCharacterAttack.Fspecial )
	end
	self:SetNetPropBoolean( IsFast, fast )
	self:SetNetPropInt32( LifeTimer, 0 )

	local charged = Hodan2_Shared.NextWhirlCharged
	self:SetNetPropInt32( Level, 1 )
	self:SetNetPropInt32( LastSprite, 0 )

	local dir       = ( InFacing == ERivalsFacingDirection.Right ) and 1.0 or -1.0
	local base_hsp  = ( fast or charged ) and 7.0 or 3.0
	local boost     = charged and 1.4 or 1.0
	local arcing    = fast and not charged
	local hsp       = base_hsp * SCALE * dir * boost
	local vsp       = arcing and ( 5.0 * SCALE ) or 0.0
	self:SetVelocity( Vector2D:new( hsp, vsp ) )
end

local function AnimKeyForLevel( level )
	if ( level >= 3 ) then return "sweatwhirl_proj3" end
	if ( level >= 2 ) then return "sweatwhirl_proj2" end
	return "sweatwhirl_proj"
end

function Sweatwhirl:ArticleUpdate()
	self:Super_ArticleUpdate()

	if ( self:GetNetPropBoolean( Caught ) ) then
		local owner = self:GetOwnerRival()
		if ( owner ~= nil ) then
			local op = owner:GetLocation2D()
			local dir = owner:GetFacingDirectionFloat()
			self:MoveToLocation( Vector2D:new( op.X + 30.0 * dir, op.Y + 80.0 ) )
		end
		self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )
		return
	end

	local t = self:GetNetPropInt32( LifeTimer ) + 1
	self:SetNetPropInt32( LifeTimer, t )

	Sweatwhirl.CheckVapourLevel( self )

	local lvl = self:GetNetPropInt32( Level )
	if ( lvl ~= self:GetNetPropInt32( LastSprite ) ) then
		self:Set2DAnimation( AnimKeyForLevel( lvl ) )
		self:SetNetPropInt32( LastSprite, lvl )
	end

	local life = self:GetNetPropBoolean( IsFast ) and 120 or 170
	if ( t >= life ) then
		self:Deactivate()
	end
end

function Sweatwhirl:OnDeactivated()
	if ( self:GetNetPropBoolean( Bashed ) ) then return end
	if ( self:GetNetPropBoolean( Caught ) ) then return end
	if ( self:GetNetPropInt32( LifeTimer ) > 5 ) then
		Sweatwhirl.SpawnVapourOnDeath( self )
		self:SpawnVfx( "sweatwhirlhit" )
	end
end

function Sweatwhirl:OnParried()
	self:SetNetPropBoolean( Bashed, true )
	self:Deactivate()
end

function Sweatwhirl:OnHitRival( OtherRival, Hitbox )
	self:ApplyHitpauseDirect( OtherRival:GetRemainingHitpauseFrames() )
	local hc = self:GetNetPropInt32( HitCount ) + 1
	self:SetNetPropInt32( HitCount, hc )
	local level = self:GetNetPropInt32( Level )
	if ( level < 3 and hc >= level ) then self:Deactivate() end
end
function Sweatwhirl:OnHitGround( HitPosition )
	self:PlaySFX( "sfx_stinky_steam2" )
	self:Deactivate()
end
function Sweatwhirl:OnHitWall( HitPosition )
	self:PlaySFX( "sfx_stinky_steam2" )
	self:Deactivate()
end

function Sweatwhirl:CheckVapourLevel()
	local owner = self:GetOwnerRival()
	if ( owner == nil ) then return end
	local lvl = self:GetNetPropInt32( Level )
	if ( lvl >= 3 ) then return end
	local vaps = owner:GetMyArticlesTableByName( "Vapour" )
	if ( vaps == nil ) then return end
	local p = self:GetLocation2D()
	local r = 75.0 * SCALE
	for _, vap in pairs( vaps ) do
		if ( not Vapour.IsDying( vap ) ) then
		local vp = vap:GetLocation2D()
		local dx, dy = vp.X - p.X, vp.Y - p.Y
		if ( ( dx * dx + dy * dy ) < ( r * r ) ) then
			if     ( lvl == 1 ) then self:PlaySFX( "sfx_stinky_steam1" )
			elseif ( lvl == 2 ) then self:PlaySFX( "sfx_stinky_steam2" ) end
			self:SetNetPropInt32( Level, math.min( 3, lvl + 1 ) )
			Vapour.StartDying( vap )
			return
		end
		end
	end
end

function Sweatwhirl:SpawnVapourOnDeath()
	local owner = self:GetOwnerRival()
	if ( owner == nil ) then return end
	local vap_ad = GetVapourAD()
	if ( vap_ad == nil ) then return end

	local existing = owner:GetMyArticlesTableByName( "Vapour" )
	if ( existing ~= nil ) then
		local count, first = 0, nil
		for _, v in pairs( existing ) do
			count = count + 1
			if ( first == nil ) then first = v end
		end
		if ( count >= 3 and first ~= nil ) then first:Deactivate() end
	end
	local vap = owner:CreateArticle( vap_ad, Vector2D:new( 0.0, 0.0 ), 1.0, "First" )
	if ( vap ~= nil ) then vap:MoveToLocation( self:GetLocation2D() ) end
end

function Sweatwhirl:GetActiveHitboxes( bIgnoreHitboxLocation )
	if ( self:GetNetPropBoolean( Caught ) ) then return true end
	local fast = self:GetNetPropBoolean( IsFast )
	local lvl  = self:GetNetPropInt32( Level )
	local dmg    = ( fast and 3 or 2 ) + ( lvl - 1 ) * 2
	local bkb    = ( fast and 7.0 or 5.0 ) + ( lvl - 1 ) * 2.0
	local kbs    = fast and 0.2 or 0.1
	local angle  = fast and 50 or 60
	if ( self:GetNetPropBoolean( Thrown ) ) then angle = 270 end
	local radius = 24.0 + ( lvl - 1 ) * 14.0
	local hit_sound
	if ( lvl >= 2 ) then hit_sound = "sfx_stinky_steam2"
	elseif ( fast )  then hit_sound = "sfx_stinky_steam1"
	else                  hit_sound = "sfx_stinky_steam2" end

	local base_hitpause
	if     ( lvl >= 3 ) then base_hitpause = 2
	elseif ( lvl >= 2 ) then base_hitpause = 8
	else                     base_hitpause = 4 end
	local rehit_frames = ( lvl >= 3 ) and 10 or 0

	self:Lua_AppendHitbox(
		self:GetAttack(),
		1,
		self:GetNetPropInt32( LifeTimer ),
		2,
		Vector.new( 0.0, 0.0, 0.0 ),
		radius,
		dmg,
		bkb,
		kbs,
		angle,
		base_hitpause,
		0.25,
		0,
		1.0,
		0.0,
		1,
		0.5,
		false,
		true,
		rehit_frames,
		hit_sound,
		""
	)
	return true
end
