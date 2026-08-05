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
local Bashed    = nil
local Caught    = nil
local Thrown    = nil
local Charged   = nil
local DmgBonus  = nil
local PopTimer  = nil
local LeveledHit  = nil
local LeveledTmr  = nil

local RealDeath = nil

local POP_LEN = 3
local LEVELED_RESET = 20

local function DieForReal( self )
	self:SetNetPropBoolean( RealDeath, true )
	self:Deactivate()
end

function Sweatwhirl:RegisterNetProps()
	IsFast     = self:AddNetPropBoolean()
	LifeTimer  = self:AddNetPropInt32()
	Level      = self:AddNetPropInt32()
	LastSprite = self:AddNetPropInt32()
	PopTimer   = self:AddNetPropInt32()
	LeveledHit = self:AddNetPropBoolean()
	LeveledTmr = self:AddNetPropInt32()
	Bashed     = self:AddNetPropBoolean()
	Caught     = self:AddNetPropBoolean()
	Thrown     = self:AddNetPropBoolean()
	Charged    = self:AddNetPropBoolean()
	DmgBonus   = self:AddNetPropInt32()
	RealDeath  = self:AddNetPropBoolean()
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
	DieForReal( self )
end

function Sweatwhirl:DropSilent()
	self:SetNetPropBoolean( Caught, false )
	self:SetNetPropBoolean( Bashed, true )
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
	self:SetNetPropBoolean( Charged, charged and true or false )
	self:SetNetPropInt32( Level, 1 )
	self:SetNetPropInt32( DmgBonus, tonumber( Hodan2_Shared.NextWhirlDmgBonus ) or 0 )
	self:SetNetPropInt32( LastSprite, 0 )

	if ( Hodan2_Shared.NextWhirlSpikeToss ) then
		Hodan2_Shared.NextWhirlSpikeToss = false
		self:SetNetPropBoolean( Thrown, true )
		self:SetVelocity( Vector2D:new( 0.0, -10.0 * SCALE ) )
		return
	end

	local dir       = ( InFacing == ERivalsFacingDirection.Right ) and 1.0 or -1.0
	local hsp_px    = charged and 11.0 or ( fast and 7.0 or 3.0 )
	local arcing    = fast and not charged
	local hsp       = hsp_px * SCALE * dir
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

	local pop = self:GetNetPropInt32( PopTimer )
	if ( pop > 0 ) then
		self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )
		pop = pop - 1
		self:SetNetPropInt32( PopTimer, pop )
		if ( pop <= 0 ) then DieForReal( self ) end
		return
	end

	local t = self:GetNetPropInt32( LifeTimer ) + 1
	self:SetNetPropInt32( LifeTimer, t )

	local ltmr = self:GetNetPropInt32( LeveledTmr )
	if ( ltmr > 0 ) then
		ltmr = ltmr - 1
		self:SetNetPropInt32( LeveledTmr, ltmr )
		if ( ltmr == 0 ) then self:SetNetPropBoolean( LeveledHit, false ) end
	end

	Sweatwhirl.CheckVapourLevel( self )

	local lvl = self:GetNetPropInt32( Level )
	if ( lvl ~= self:GetNetPropInt32( LastSprite ) ) then
		self:Set2DAnimation( AnimKeyForLevel( lvl ) )
		self:SetNetPropInt32( LastSprite, lvl )
	end

	local life = self:GetNetPropBoolean( IsFast ) and 200 or 900
	if ( t >= life ) then
		DieForReal( self )
	end
end

function Sweatwhirl:OnDeactivated()
	if ( self:GetNetPropBoolean( Bashed ) ) then return end
	if ( self:GetNetPropBoolean( Caught ) ) then return end
	if ( self:GetNetPropBoolean( RealDeath ) ) then
		Sweatwhirl.SpawnVapourOnDeath( self )
		self:SpawnVfx( "stinky_sweatwhirl_fx" )
	end
end

function Sweatwhirl:OnParried()
	self:SetNetPropBoolean( Bashed, true )
	self:Deactivate()
end

local function DeathSfxName( self )
	if ( self:GetNetPropBoolean( IsFast ) or self:GetNetPropBoolean( Charged ) ) then
		return "sfx_stinky_steam1"
	end
	return "sfx_stinky_steam2"
end

function Sweatwhirl:OnHitRival( OtherRival, Hitbox )
	local id = Hitbox and Hitbox.HitboxID or 1
	if ( id == 2 ) then
		local lvl = self:GetNetPropInt32( Level )
		self:SetNetPropBoolean( LeveledHit, true )
		self:SetNetPropInt32( LeveledTmr, LEVELED_RESET )
		self:ApplyHitpauseDirect( lvl == 2 and 4 or 8 )
		return
	end
	if ( id == 3 ) then return end
	if ( self:GetNetPropInt32( PopTimer ) > 0 ) then return end
	self:PlaySFX( DeathSfxName( self ) )
	if ( self:GetNetPropBoolean( Charged ) ) then
		self:MoveToLocation( OtherRival:GetLocation2D() )
		self:SetNetPropInt32( PopTimer, OtherRival:GetRemainingHitpauseFrames() + 1 + POP_LEN )
		self:SetVelocity( Vector2D:new( 0.0, 0.0 ) )
	else
		DieForReal( self )
	end
end
function Sweatwhirl:OnHitGround( HitPosition )
	self:PlaySFX( DeathSfxName( self ) )
	DieForReal( self )
end
function Sweatwhirl:OnHitWall( HitPosition )
	self:PlaySFX( DeathSfxName( self ) )
	DieForReal( self )
end

function Sweatwhirl:CheckVapourLevel()
	local owner = self:GetOwnerRival()
	if ( owner == nil ) then return end
	local lvl = self:GetNetPropInt32( Level )
	if ( lvl >= 3 ) then return end
	local vaps = owner:GetMyArticlesTableByName( "Vapour" )
	if ( vaps == nil ) then return end
	local p = self:GetLocation2D()
	local rx = 100.0
	local ry = 125.0
	for _, vap in pairs( vaps ) do
		if ( not Vapour.IsDying( vap ) ) then
		local vp = vap:GetLocation2D()
		local dx, dy = vp.X - p.X, vp.Y - p.Y
		if ( dx >= -rx and dx <= rx and dy >= -ry and dy <= ry ) then
			if     ( lvl == 1 ) then self:PlaySFX( "sfx_stinky_steam1" )
			elseif ( lvl == 2 ) then self:PlaySFX( "sfx_stinky_steam2" ) end
			self:SetNetPropInt32( Level, math.min( 3, lvl + 1 ) )
			self:SetNetPropBoolean( LeveledHit, false )
			self:SetNetPropInt32( LeveledTmr, 0 )
			vap:SpawnVfx( "water_light_omni_spr" )
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

local MAIN_RADIUS = { 80.0, 95.0, 130.0 }

function Sweatwhirl:GetActiveHitboxes( bIgnoreHitboxLocation )
	if ( self:GetNetPropBoolean( Caught ) ) then return true end
	local fast    = self:GetNetPropBoolean( IsFast )
	local charged = self:GetNetPropBoolean( Charged )
	local lvl     = self:GetNetPropInt32( Level )
	local frames  = self:GetNetPropInt32( LifeTimer )

	local pop = self:GetNetPropInt32( PopTimer )
	if ( pop > 0 ) then
		if ( pop <= POP_LEN ) then
			local pop_bkb = 6.0
			if     ( lvl >= 3 ) then pop_bkb = 12.0
			elseif ( lvl >= 2 ) then pop_bkb = 10.0 end
			self:Lua_AppendHitbox(
				self:GetAttack(), 3, POP_LEN - pop, POP_LEN,
				Vector.new( 0.0, 0.0, 0.0 ),
				75.0,
				1,
				pop_bkb, 0.4, 55,
				8, 0.25, 0,
				1.0, 0.0, 1,
				0.7, false,
				true,
				0, "sfx_stinky_steam2", ""
			)
		end
		return true
	end

	local leveled   = lvl >= 2
	local pull_live = leveled and ( lvl >= 3 or not self:GetNetPropBoolean( LeveledHit ) )
	local main_live = not pull_live

	local sb = self:GetNetPropInt32( DmgBonus )
	if ( fast and sb > 0 ) then sb = sb - 1 end
	local dmg = ( fast and 3 or 2 ) + sb
	local bkb = fast and 7.0 or 5.0
	if ( not charged ) then
		if     ( lvl >= 3 ) then bkb = fast and 11.0 or 5.0
		elseif ( lvl >= 2 ) then bkb = fast and 9.0 or 7.0 end
	end
	local kbs   = fast and 0.2 or 0.1
	local angle = fast and 50 or 60
	if ( self:GetNetPropBoolean( Thrown ) ) then angle = 270 end
	local radius = MAIN_RADIUS[ math.min( lvl, 3 ) ]
	local hit_sound = fast and "sfx_stinky_steam1" or "sfx_stinky_steam2"

	if ( main_live ) then
	self:Lua_AppendHitbox(
		self:GetAttack(), 1, frames, 2,
		Vector.new( 0.0, 0.0, 0.0 ),
		radius,
		dmg,
		bkb, kbs, angle,
		4, 0.25, 0,
		1.0, 0.0, 1,
		0.5, false,
		( not fast ) and ( not charged ),
		4,
		hit_sound, ""
	)
	end

	if ( pull_live ) then
		local v = self:GetVelocity2D()
		local offz = v.Y
		if ( self:GetNetPropBoolean( Thrown ) ) then offz = offz + 70.0 end
		local pull_dmg
		if ( lvl >= 3 ) then pull_dmg = charged and 2 or 1
		else                 pull_dmg = charged and 3 or 2 end
		self:Lua_AppendHitbox(
			self:GetAttack(), 2, frames, 2,
			Vector.new( v.X, 0.0, offz ),
			80.0,
			pull_dmg,
			4.0, 0.0, 0,
			2, 0.0, 0,
			0.01, 0.0, 1,
			1.0, false,
			true,
			( lvl >= 3 ) and 2 or 4,
			"sfx_stinky_steam2", ""
		)
	end
	return true
end
