Hodan2 = Class( RivalsLua2DCharacterEntity )

local SCALE = 2.5

local FAIR_CHARGED    = ERivalsCharacterAttack.Extra1
local DSTRONG_CHARGED = ERivalsCharacterAttack.Extra2
local SPECIAL_FALL    = ERivalsCharacterAttack.Extra4
local function IsFairAttack( atk )
	return atk == ERivalsCharacterAttack.Fair or atk == FAIR_CHARGED
end

local STEAM_CHARGE = 0.04
local STEAM_DECAY  = 0.08
local STEAM_BUFFER = 10
local STEAM_VIS    = 0.7
local JAB_LOOP_WINDOW = 2

Hodan2_Shared = Hodan2_Shared or {}
Hodan2_Shared.NextWhirlCharged     = false
Hodan2_Shared.NextVapourIsParry    = false
Hodan2_Shared.ForceFast            = false
Hodan2_Shared.NextAfterimageKey      = ""
Hodan2_Shared.NextAfterimageMode     = ""
Hodan2_Shared.NextAfterimageLifetime = 0
Hodan2_Shared.NextSteamParticleKey   = ""

local MOD_UA_ROOT = "/Game/ModContent/3752556104/UnrealAssets/Articles/"
local MOD_PA_ROOT = "/Game/ModContent/3752556104/PublishedAssets/Articles/"
local function LoadArticleByName( name )
	return LoadArticleData( MOD_UA_ROOT .. name ) or LoadArticleData( MOD_PA_ROOT .. name )
end
local function GetSweatwhirlAD()
	Hodan2_Shared.SweatwhirlAD = Hodan2_Shared.SweatwhirlAD or LoadArticleByName( "AD_Hodan2_Sweatwhirl" )
	return Hodan2_Shared.SweatwhirlAD
end
local function GetVapourAD()
	Hodan2_Shared.VapourAD = Hodan2_Shared.VapourAD or LoadArticleByName( "AD_Hodan2_Vapour" )
	return Hodan2_Shared.VapourAD
end
local function GetAfterimageAD()
	Hodan2_Shared.AfterimageAD = Hodan2_Shared.AfterimageAD or LoadArticleByName( "AD_Hodan2_Afterimage" )
	return Hodan2_Shared.AfterimageAD
end
local function GetSteamParticleAD()
	Hodan2_Shared.SteamParticleAD = Hodan2_Shared.SteamParticleAD or LoadArticleByName( "AD_Hodan2_SteamParticle" )
	return Hodan2_Shared.SteamParticleAD
end

local SteamH      = nil
local SteamV      = nil
local SteamHBuf   = nil
local SteamVBuf   = nil
local SpecSpawned = nil
local Holding     = nil
local EcbTall     = nil
local LatchArmed  = nil
local LatchH      = nil
local LatchFwd    = nil
local LatchBwd    = nil
local LatchV      = nil
local UspBoosted  = nil
local DstrArmored = nil
local AnimOverride = nil
local JabCancel = nil
local JabLoopArmed = nil
local NairJc = nil
local DspecJc = nil
local DspecThrew = nil
local UspecLanded = nil
local PrevAttackEnum = nil
local LastNonNoneAttack = nil
local InVapourFrame = nil
local HeldWhirlLevel = nil
local WindupFlashFired = nil
local JabShakePlaying = nil

local function GetSteam( ent, handle ) return ent:GetNetPropInt32( handle ) / 100.0 end
local function SetSteam( ent, handle, v ) ent:SetNetPropInt32( handle, math.floor( v * 100.0 + 0.5 ) ) end


function Hodan2:RegisterNetProps()
	SteamH       = self:AddNetPropInt32()
	SteamV       = self:AddNetPropInt32()
	SteamHBuf    = self:AddNetPropInt32()
	SteamVBuf    = self:AddNetPropInt32()
	SpecSpawned  = self:AddNetPropBoolean()
	Holding      = self:AddNetPropBoolean()
	EcbTall      = self:AddNetPropBoolean()
	LatchArmed   = self:AddNetPropBoolean()
	LatchH       = self:AddNetPropBoolean()
	LatchFwd     = self:AddNetPropBoolean()
	LatchBwd     = self:AddNetPropBoolean()
	LatchV       = self:AddNetPropBoolean()
	UspBoosted   = self:AddNetPropBoolean()
	DstrArmored    = self:AddNetPropBoolean()
	AnimOverride   = self:AddNetPropBoolean()
	JabCancel      = self:AddNetPropBoolean()
	JabLoopArmed   = self:AddNetPropBoolean()
	NairJc         = self:AddNetPropBoolean()
	DspecJc        = self:AddNetPropBoolean()
	DspecThrew     = self:AddNetPropBoolean()
	UspecLanded    = self:AddNetPropBoolean()
	PrevAttackEnum = self:AddNetPropInt32()
	LastNonNoneAttack = self:AddNetPropInt32()
	InVapourFrame = self:AddNetPropInt32()
	HeldWhirlLevel = self:AddNetPropInt32( 1, 3 )
	WindupFlashFired = self:AddNetPropBoolean()
	JabShakePlaying = self:AddNetPropBoolean()
end

function Hodan2:SetAttack( InAttack, InputFramesAgo, bRightStick )
	if ( InAttack == ERivalsCharacterAttack.Fair ) then
		local h = GetSteam( self, SteamH )
		local facing = self:GetFacingDirectionFloat()
		if ( ( h * facing ) >= 0.85 ) then
			return self:Super_SetAttack( FAIR_CHARGED, InputFramesAgo, bRightStick )
		end
	elseif ( InAttack == ERivalsCharacterAttack.Dstrong and self:IsGrounded() ) then
		local v = GetSteam( self, SteamV )
		if ( v <= -0.85 ) then
			return self:Super_SetAttack( DSTRONG_CHARGED, InputFramesAgo, bRightStick )
		end
	elseif ( InAttack == ERivalsCharacterAttack.Dspecial ) then
		if ( not self:IsGrounded()
				and self:GetAttackCountPerAirtime( ERivalsCharacterAttack.Dspecial ) > 0 ) then
			return false
		end
	end
	return self:Super_SetAttack( InAttack, InputFramesAgo, bRightStick )
end

function Hodan2:UpdateSteam()
	local frame = self:GetMatchFrame()
	local right = self:IsRightDown()
	local left  = self:IsLeftDown()
	local down  = self:IsDownDown() and not self:IsUpDown()

	local h = GetSteam( self, SteamH )
	if right and not left then
		h = math.min( 1.0, h + STEAM_CHARGE )
		self:SetNetPropInt32( SteamHBuf, frame )
	elseif left and not right then
		h = math.max( -1.0, h - STEAM_CHARGE )
		self:SetNetPropInt32( SteamHBuf, frame )
	elseif frame - self:GetNetPropInt32( SteamHBuf ) > STEAM_BUFFER then
		if h > STEAM_DECAY then h = h - STEAM_DECAY
		elseif h < -STEAM_DECAY then h = h + STEAM_DECAY
		else h = 0.0 end
	end
	SetSteam( self, SteamH, h )

	local v = GetSteam( self, SteamV )
	if down then
		v = math.max( -1.0, v - STEAM_CHARGE )
		self:SetNetPropInt32( SteamVBuf, frame )
	elseif frame - self:GetNetPropInt32( SteamVBuf ) > STEAM_BUFFER then
		if v < -STEAM_DECAY then v = v + STEAM_DECAY else v = 0.0 end
	end
	SetSteam( self, SteamV, v )
end

function Hodan2:MaxSteamFromVapour()
	local facing = self:GetFacingDirectionFloat()
	SetSteam( self, SteamH, facing )
	SetSteam( self, SteamV, -1.0 )
	local frame = self:GetMatchFrame()
	self:SetNetPropInt32( SteamHBuf, frame )
	self:SetNetPropInt32( SteamVBuf, frame )
	self:SetNetPropInt32( InVapourFrame, frame )
end

local function IsInVapour( ent )
	local last = ent:GetNetPropInt32( InVapourFrame )
	return ( ent:GetMatchFrame() - last ) <= 1
end

function Hodan2:UpdateSteamVisual()
	local h = math.abs( GetSteam( self, SteamH ) )
	local v = math.abs( GetSteam( self, SteamV ) )
	if ( h > STEAM_VIS or v > STEAM_VIS ) then
		local red = math.min( 255, math.floor( 70 * ( h + v ) ) )
		self:SetOutlineTint( red, 0, 0 )
	else
		self:SetOutlineTint( -1, -1, -1 )
	end
end

function Hodan2:UpdateSteamLatch()
	local atk  = self:GetAttack()
	local prev = self:GetNetPropInt32( PrevAttackEnum )
	self:SetNetPropInt32( PrevAttackEnum, atk )

	if ( atk == ERivalsCharacterAttack.None or atk ~= prev ) then
		self:SetNetPropBoolean( LatchArmed, true )
	end
	if ( atk == ERivalsCharacterAttack.None ) then return end
	if ( not self:GetNetPropBoolean( LatchArmed ) ) then return end
	self:SetNetPropBoolean( LatchArmed, false )

	local h = GetSteam( self, SteamH )
	local v = GetSteam( self, SteamV )
	local facing = self:GetFacingDirectionFloat()
	local in_vap = IsInVapour( self )
	self:SetNetPropBoolean( LatchH,   math.abs( h ) >= 0.85 )
	self:SetNetPropBoolean( LatchFwd, ( h * facing ) >=  0.85 )
	self:SetNetPropBoolean( LatchBwd, in_vap or ( h * facing ) <= -0.85 )
	self:SetNetPropBoolean( LatchV,   v <= -0.85 )
	self:SetNetPropBoolean( UspBoosted,     false )
	self:SetNetPropBoolean( JabCancel,      false )
	self:SetNetPropBoolean( JabLoopArmed,   false )
	self:SetNetPropBoolean( NairJc,         false )
	self:SetNetPropBoolean( DspecJc,        false )
	self:SetNetPropBoolean( DspecThrew,     false )
	self:SetNetPropBoolean( UspecLanded,    false )
	self:SetNetPropBoolean( WindupFlashFired, false )
end

function Hodan2:OnHitRival( OtherRival, Hitbox )
	self:Super_OnHitRival( OtherRival, Hitbox )
	if ( OtherRival == nil ) then return end

	local attack = self:GetAttack()
	local hbox   = Hitbox.HitboxID


	if ( attack == ERivalsCharacterAttack.Jab and hbox == 0 ) then
		self:SetNetPropBoolean( JabCancel, true )
	elseif ( attack == ERivalsCharacterAttack.Nair ) then
		self:SetNetPropBoolean( NairJc, true )
	elseif ( attack == ERivalsCharacterAttack.Dspecial ) then
		self:SetNetPropBoolean( DspecJc, true )
	end

	if ( attack == ERivalsCharacterAttack.Uair ) then
		local v = self:GetVelocity2D()
		self:SetVelocityVertical( math.max( v.Y, 4.0 ) )
	end

	if ( attack == ERivalsCharacterAttack.Dspecial and hbox == 1
			and self:WasGroundedAtFrameStart() ) then
		local v = OtherRival:GetKnockbackVelocity()
		OtherRival:SetKnockbackVelocity( Vector2D:new( v.X * 0.4, v.Y * 0.4 ) )
		self:PlaySFX( "sfx_blow_weak2" )
	end

	local plays_steam =
		attack == ERivalsCharacterAttack.Ftilt
		or attack == ERivalsCharacterAttack.Dtilt
		or attack == ERivalsCharacterAttack.Utilt
		or attack == ERivalsCharacterAttack.Uair
		or ( attack == ERivalsCharacterAttack.DAttack and self:GetNetPropBoolean( LatchFwd ) and hbox == 1 )
		or ( ( attack == ERivalsCharacterAttack.Uspecial or attack == ERivalsCharacterAttack.UspecialAir ) and hbox == 1 )
		or ( attack == ERivalsCharacterAttack.Dspecial and self:WasGroundedAtFrameStart() and hbox == 1 )
		or ( attack == DSTRONG_CHARGED )
	if ( plays_steam ) then
		self:PlaySFX( "sfx_stinky_steam1" )
		self:SpawnVfx( "stinky_splash_fx" )
	end

	local h_charged = self:GetNetPropBoolean( LatchH )
	local v_charged = self:GetNetPropBoolean( LatchV )

	if ( v_charged and ( attack == ERivalsCharacterAttack.Uspecial
			or attack == ERivalsCharacterAttack.UspecialAir ) ) then
		self:PlaySFX( "sfx_blow_heavy2" )
		self:SpawnVfx( "stinky_uspecial_charged_fx" )
	end

	if ( h_charged and attack == ERivalsCharacterAttack.DAttack ) then
		self:PlaySFX( "sfx_blow_heavy2" )
	end

	if ( not h_charged ) then return end

	local bonus = v_charged and 3 or 2
	local scale = v_charged and 1.22 or 1.15
	OtherRival:TakeDamage( bonus )
	local v = OtherRival:GetKnockbackVelocity()
	OtherRival:SetKnockbackVelocity( Vector2D:new( v.X * scale, v.Y * scale ) )
end

function Hodan2:OnGrabSuccess( Hitbox, GrabVictim )
	self:Super_OnGrabSuccess( Hitbox, GrabVictim )
	if ( self:GetAttack() == ERivalsCharacterAttack.Ustrong ) then
		self:ApplyHitpauseDirect( 10 )
		if ( GrabVictim ~= nil ) then GrabVictim:SetVisible( false ) end
	end
end

function Hodan2:UpdateChargedDstrong()
	local atk = self:GetAttack()
	local win = self:GetWindow()
	local want = atk == DSTRONG_CHARGED
		and ( ( win == 1 and self:GetWindowTimer() >= 11 ) or win == 2 )
	local active = self:GetNetPropBoolean( DstrArmored )
	if ( want and not active ) then
		self:SetNetPropBoolean( DstrArmored, true )
		self:SetArmor( 255 )
		self:PlaySFX( "sfx_parry_use" )
	elseif ( active and not want ) then
		self:SetNetPropBoolean( DstrArmored, false )
		self:SetArmor( 0 )
	end
end

function Hodan2:ArmorHitbox( Hitbox )
	self:Super_ArmorHitbox( Hitbox )
	if ( not self:GetNetPropBoolean( DstrArmored ) ) then return end

	self:ParryHitbox( Hitbox )

	local vap_ad = GetVapourAD()
	if ( vap_ad ~= nil ) then
		Hodan2_Shared.NextVapourIsParry = true
		local vap = self:CreateArticle( vap_ad, Vector2D:new( 0.0, 0.0 ), 1.0, "First" )
		if ( vap ~= nil ) then vap:MoveToLocation( self:GetLocation2D() ) end
	end

	self:PlaySFX( "sfx_stinky_steam2" )
end

function Hodan2:UpdateChargedSprites()
	local atk = self:GetAttack()
	local want, key = false, nil
	if ( atk == ERivalsCharacterAttack.DAttack and self:GetNetPropBoolean( LatchFwd ) ) then
		want, key = true, "dattack_strong"
	end
	local active = self:GetNetPropBoolean( AnimOverride )
	if ( want and not active ) then
		self:Set2DAnimation( key )
		self:SetNetPropBoolean( AnimOverride, true )
	elseif ( active and not want ) then
		self:Set2DAnimation( "" )
		self:SetNetPropBoolean( AnimOverride, false )
	end
end

function Hodan2:UpdateUtiltHeight()
	local tall = ( self:GetAttack() == ERivalsCharacterAttack.Utilt ) and ( self:GetWindow() == 2 )
	if ( tall ) then
		if ( not self:GetNetPropBoolean( EcbTall ) ) then
			self:Set2DEcb( self:GetECBWidth(), self:GetECBHeight() * 1.42 )
			self:SetNetPropBoolean( EcbTall, true )
		end
	elseif ( self:GetNetPropBoolean( EcbTall ) ) then
		self:Set2DEcb( 0, 0 )
		self:SetNetPropBoolean( EcbTall, false )
	end
end


local function AfterimageKeyForAttack( ent )
	local atk = ent:GetAttack()
	if ( ( atk == ERivalsCharacterAttack.Uspecial or atk == ERivalsCharacterAttack.UspecialAir )
			and ent:GetNetPropBoolean( LatchV ) ) then
		return "uspecialflash"
	elseif ( ( atk == ERivalsCharacterAttack.Fspecial or atk == ERivalsCharacterAttack.Nspecial )
			and ent:GetNetPropBoolean( LatchBwd ) ) then
		return "fspecialflash"
	end
	return nil
end

function Hodan2:UpdateAfterimage()
	local key = AfterimageKeyForAttack( self )
	if ( key == nil ) then return end
	local ad = GetAfterimageAD()
	if ( ad == nil ) then return end
	Hodan2_Shared.NextAfterimageKey  = key
	Hodan2_Shared.NextAfterimageMode = "trail"
	self:CreateArticle( ad, Vector2D:new( 0.0, 0.0 ), 1.0, "First" )
end

function Hodan2:UpdateChargedFlashOverlay()
	local atk = self:GetAttack()
	local win = self:GetWindow()
	local wt  = self:GetWindowTimer()
	local wl  = self:GetWindowLength()

	local windup_key = nil
	if ( IsFairAttack( atk ) and win == 1
			and wt >= wl - 3 and self:GetNetPropBoolean( LatchFwd ) ) then
		windup_key = "fair_strong_flash"
	elseif ( atk == ERivalsCharacterAttack.DAttack and win == 1
			and wt >= wl - 3 and self:GetNetPropBoolean( LatchFwd ) ) then
		windup_key = "dattack_strong_flash"
	elseif ( atk == DSTRONG_CHARGED and win == 2
			and wt >= 3 and wt <= 5 ) then
		windup_key = "dstrong_strong_flash"
	end
	if ( windup_key ~= nil and not self:GetNetPropBoolean( WindupFlashFired ) ) then
		self:SetNetPropBoolean( WindupFlashFired, true )
		local ad = GetAfterimageAD()
		if ( ad ~= nil ) then
			Hodan2_Shared.NextAfterimageKey      = windup_key
			Hodan2_Shared.NextAfterimageMode     = "static"
			Hodan2_Shared.NextAfterimageLifetime = 3
			self:CreateArticle( ad, Vector2D:new( 0.0, 0.0 ), 1.0, "First" )
		end
	end

	local flicker_key = nil
	if ( ( atk == ERivalsCharacterAttack.Uspecial or atk == ERivalsCharacterAttack.UspecialAir )
			and self:GetNetPropBoolean( LatchV ) and win < 4 ) then
		flicker_key = "uspecialflash2"
	elseif ( ( atk == ERivalsCharacterAttack.Fspecial or atk == ERivalsCharacterAttack.Nspecial )
			and self:GetNetPropBoolean( LatchBwd ) ) then
		flicker_key = "fspecialflash2"
	end
	if ( flicker_key ~= nil and ( self:GetMatchFrame() % 8 ) == 0 ) then
		local ad = GetAfterimageAD()
		if ( ad ~= nil ) then
			Hodan2_Shared.NextAfterimageKey      = flicker_key
			Hodan2_Shared.NextAfterimageMode     = "static"
			Hodan2_Shared.NextAfterimageLifetime = 2
			self:CreateArticle( ad, Vector2D:new( 0.0, 0.0 ), 1.0, "First" )
		end
	end
end

function Hodan2:UpdateSteamParticles()
	local h = math.abs( GetSteam( self, SteamH ) )
	local v = math.abs( GetSteam( self, SteamV ) )
	if ( h <= STEAM_VIS and v <= STEAM_VIS ) then return end
	if ( self:GetRandomFloat() >= 0.10 ) then return end

	local ad = GetSteamParticleAD()
	if ( ad == nil ) then return end

	local idx = self:GetRandomIntRange( 1, 8 )
	Hodan2_Shared.NextSteamParticleKey = "steamparticle" .. idx
	local jitter_x = ( self:GetRandomFloat() - 0.5 ) * 60.0
	local jitter_y = ( self:GetRandomFloat() - 0.5 ) * 60.0
	self:CreateArticle( ad, Vector2D:new( jitter_x, 30.0 + jitter_y ), 1.0, "First" )
end

function Hodan2:UpdateState()
	self:Super_UpdateState()
	Hodan2.UpdateSteam( self )
	Hodan2.UpdateSteamVisual( self )
	Hodan2.UpdateSteamLatch( self )
	Hodan2.UpdateChargedDstrong( self )
	Hodan2.UpdateChargedSprites( self )
	Hodan2.UpdateAfterimage( self )
	Hodan2.UpdateChargedFlashOverlay( self )
	Hodan2.UpdateSteamParticles( self )
	Hodan2.UpdateHeldWhirl( self )
	Hodan2.UpdateUtiltHeight( self )
	Hodan2.MaybeEnterSpecialFall( self )
	Hodan2.UpdateJabShake( self )
	Hodan2.ResolveUstrongGrabFacing( self )
end

function Hodan2:ResolveUstrongGrabFacing()
	if ( self:GetAttack() ~= ERivalsCharacterAttack.Ustrong ) then return end
	if ( self:GetWindow() ~= 4 or self:GetWindowTimer() ~= 0 ) then return end
	if ( self:GetGrabPartner() == nil ) then return end
	local facing = self:GetFacingDirection()
	if ( self:IsLeftDown() and facing == ERivalsFacingDirection.Right ) then
		self:SetFacingDirection( ERivalsFacingDirection.Left )
	elseif ( self:IsRightDown() and facing == ERivalsFacingDirection.Left ) then
		self:SetFacingDirection( ERivalsFacingDirection.Right )
	end
end

function Hodan2:UpdateJabShake()
	local in_loop = (
		self:GetAttack() == ERivalsCharacterAttack.Jab
		and self:GetWindow() == JAB_LOOP_WINDOW
	)
	local playing = self:GetNetPropBoolean( JabShakePlaying )
	if ( in_loop ) then
		local timer = self:GetWindowTimer()
		if ( not playing or timer == 0 ) then
			if ( playing ) then self:StopSFX( "sfx_stinky_shake" ) end
			self:PlaySFX( "sfx_stinky_shake" )
			self:SetNetPropBoolean( JabShakePlaying, true )
		end
	elseif ( playing ) then
		self:StopSFX( "sfx_stinky_shake" )
		self:PlaySFX( "sfx_stinky_shakefade" )
		self:SetNetPropBoolean( JabShakePlaying, false )
	end
end

function Hodan2:MaybeEnterSpecialFall()
	local curr = self:GetAttack()
	if ( curr ~= ERivalsCharacterAttack.None ) then
		self:SetNetPropInt32( LastNonNoneAttack, curr )
		return
	end
	if ( self:IsGrounded() ) then return end
	local last = self:GetNetPropInt32( LastNonNoneAttack )
	if ( last == ERivalsCharacterAttack.Uspecial ) then
		self:SetAttack( SPECIAL_FALL )
	end
end

function Hodan2:MoveGrabPartner()
	local partner = self:GetGrabPartner()
	if ( partner ~= nil and self:GetAttack() == ERivalsCharacterAttack.Ustrong ) then
		local win  = self:GetWindow()
		local r1x, r1y
		local visible
		if ( win < 4 ) then
			r1x, r1y = 50, -146
			visible  = false
		elseif ( win == 4 ) then
			local tick = self:GetWindowTimer()
			local frame = math.floor( tick * 6 / 28 )
			if     ( frame == 0 ) then r1x, r1y =  50, -146; visible = false
			elseif ( frame == 1 ) then r1x, r1y =  10, -150; visible = false
			elseif ( frame == 2 ) then r1x, r1y = -16, -150; visible = false
			elseif ( frame == 3 ) then r1x, r1y = -30, -150; visible = false
			else
				local dt = math.max( 0, tick - 19 )
				r1x = -30 + 30 * dt
				r1y = math.min( -150 + 30 * dt, 0 )
				visible = true
			end
		else
			partner:SetVisible( true )
			self:Super_MoveGrabPartner()
			return
		end

		local dir  = self:GetFacingDirectionFloat()
		local hpos = self:GetLocation2D()
		partner:MoveToLocation( Vector2D:new(
			hpos.X + r1x * SCALE * dir,
			hpos.Y - r1y * SCALE
		) )
		partner:SetVisible( visible )
		return
	end
	self:Super_MoveGrabPartner()
end


function Hodan2:SpawnSweatwhirl()
	local ad = GetSweatwhirlAD()
	if ( ad == nil ) then return false end

	Hodan2_Shared.NextWhirlCharged = self:GetNetPropBoolean( LatchBwd )
	Hodan2_Shared.ForceFast        = false

	local off = Vector2D:new( 32.0 * SCALE, 38.0 * SCALE )

	local fspec   = self:GetAttack() == ERivalsCharacterAttack.Fspecial
	local charged = Hodan2_Shared.NextWhirlCharged
	local win
	if ( charged ) then
		win = "ChargedTravel"
	elseif ( fspec ) then
		win = "Arc"
	else
		win = "Travel"
	end

	self:CreateArticle( ad, off, 1.0, win )
	return true
end

function Hodan2:TryCatchSweatwhirl()
	if ( self:GetNetPropBoolean( Holding ) ) then return end
	local sws = self:GetMyArticlesTableByName( "Sweatwhirl" )
	if ( sws == nil ) then return end
	local p = self:GetLocation2D()
	local r = 75.0
	for _, sw in pairs( sws ) do
		if ( not Sweatwhirl.IsThrown( sw ) ) then
			local sp = sw:GetLocation2D()
			local dx = sp.X - p.X
			local dy = sp.Y - p.Y
			if ( ( dx * dx + dy * dy ) < ( r * r ) ) then
				self:SetNetPropBoolean( Holding, true )
				self:SetNetPropInt32( HeldWhirlLevel,
					Sweatwhirl.GetCurrentLevel( sw ) or 1 )
				Sweatwhirl.MarkCaught( sw )
				return
			end
		end
	end
end

local DSPEC_THROW_FRAME = 12
local DSPEC_W4_IDX      = 3
local DSPEC_W2_IDX      = 1
local DSPEC_W3_IDX      = 2
local DSPEC_THROW_VSP   = 10.0

local function GetHeldSweatwhirl( self )
	local sws = self:GetMyArticlesTableByName( "Sweatwhirl" )
	if ( sws == nil ) then return nil end
	for _, sw in pairs( sws ) do
		if ( sw:GetWindowName() == "Held" ) then return sw end
	end
	return nil
end

function Hodan2:UpdateHeldWhirl()
	if ( not self:GetNetPropBoolean( Holding ) ) then return end
	local a = self:GetAttack()
	local dir = self:GetFacingDirectionFloat()

	if ( a == ERivalsCharacterAttack.Dspecial
			and self:GetWindow() == DSPEC_W4_IDX
			and self:GetWindowTimer() == DSPEC_THROW_FRAME
			and not self:GetNetPropBoolean( DspecThrew ) ) then
		self:SetNetPropBoolean( DspecThrew, true )
		local sw = GetHeldSweatwhirl( self )
		if ( sw ~= nil ) then
			Sweatwhirl.ReleaseToThrow( sw, 0.0, -DSPEC_THROW_VSP * SCALE, true )
		end
		local v = self:GetVelocity2D()
		self:SetVelocityHorizontal( v.X * 0.5 )
		self:SetVelocityVertical( 8.0 * SCALE )
		self:PlaySFX( "sfx_swipe_medium2" )
		self:SetNetPropBoolean( Holding, false )
		return
	end

	if ( a == ERivalsCharacterAttack.Uspecial or a == ERivalsCharacterAttack.Dspecial ) then
		return
	end

	local sw = GetHeldSweatwhirl( self )
	if ( sw ~= nil ) then
		Sweatwhirl.DropWithVapor( sw )
	end
	self:SetNetPropBoolean( Holding, false )
end

local function HoldForward( ent, max_speed )
	local dir  = ent:GetFacingDirectionFloat()
	local want = max_speed * SCALE * dir
	local v    = ent:GetVelocity2D()
	if ( ( dir > 0 and v.X < want ) or ( dir < 0 and v.X > want ) ) then
		ent:SetVelocityHorizontal( want )
	end
end

function Hodan2:UpdateAttack()
	if ( not self:Super_UpdateAttack() ) then return false end

	local Attack = self:GetAttack()

	if ( Attack == ERivalsCharacterAttack.Nspecial or Attack == ERivalsCharacterAttack.Fspecial ) then
		local w = self:GetWindow()
		if ( w <= 1 ) then
			self:SetNetPropBoolean( SpecSpawned, false )
		elseif ( not self:GetNetPropBoolean( SpecSpawned ) ) then
			Hodan2.SpawnSweatwhirl( self )
			self:SetNetPropBoolean( SpecSpawned, true )
		end

	elseif ( Attack == ERivalsCharacterAttack.Uspecial or Attack == ERivalsCharacterAttack.UspecialAir ) then
		if ( self:GetWindow() == 1 ) then
			local v = self:GetVelocity2D()
			if ( v.Y <= 0.0 ) then
				self:SetVelocityVertical( 0.0 )
				self:SetVelocityHorizontal( 0.0 )
			end
			if ( self:GetNetPropBoolean( LatchV ) and not self:GetNetPropBoolean( UspBoosted ) ) then
				self:SetNetPropBoolean( UspBoosted, true )
				self:SetVelocityVertical( self:GetVelocity2D().Y + 6.0 * SCALE )
				self:PlaySFX( "sfx_swipe_heavy1" )
			end
		end
		if ( not self:GetNetPropBoolean( UspecLanded )
				and self:WasGroundedAtFrameStart() and self:GetWindow() >= 2 ) then
			self:SetNetPropBoolean( UspecLanded, true )
			self:SpawnVfx( "special_splash" )
		end
		Hodan2.TryCatchSweatwhirl( self )

	elseif ( Attack == ERivalsCharacterAttack.DAttack ) then
		if ( self:GetNetPropBoolean( LatchFwd ) ) then
			HoldForward( self, 9.0 )
		end

	elseif ( Attack == ERivalsCharacterAttack.Dspecial ) then
		Hodan2.TryCatchSweatwhirl( self )

		if ( self:GetWindow() == 1 and not self:GetNetPropBoolean( UspBoosted )
				and self:WasGroundedAtFrameStart() ) then
			self:SetNetPropBoolean( UspBoosted, true )
			local dir = self:GetFacingDirectionFloat()
			if ( self:IsHoldingBackward() ) then
				self:SetVelocity( Vector2D:new( -4.0 * SCALE * dir, 12.0 * SCALE ) )
			else
				self:SetVelocityHorizontal( 9.0 * SCALE * dir )
			end
		end

		if ( self:GetNetPropBoolean( DspecJc )
				and self:IsInputActionDown( ERivalsBufferedInputAction.Jump, true, true ) ) then
			self:EndAttackNaturally()
		end

		if ( self:GetNetPropBoolean( Holding )
				and self:WasGroundedAtFrameStart() ) then
			local sw = GetHeldSweatwhirl( self )
			if ( sw ~= nil ) then Sweatwhirl.DropWithVapor( sw ) end
			self:SetNetPropBoolean( Holding, false )
			self:EndAttackNaturally()
			return true
		end

		if ( self:GetNetPropBoolean( Holding ) ) then
			local w  = self:GetWindow()
			local wt = self:GetWindowTimer()
			local wl = self:GetWindowLength()
			if ( w == DSPEC_W2_IDX or w == DSPEC_W3_IDX ) then
				local hist = self:GetInputHistory()
				local p_atk  = hist:GetActionPressed( ERivalsBufferedInputAction.Attack )
				local p_spec = hist:GetActionPressed( ERivalsBufferedInputAction.Special )
				local p_str  = hist:GetActionPressed( ERivalsBufferedInputAction.Strong )
				local p_dh   = hist:GetActionPressed( ERivalsBufferedInputAction.DownHard )
				if ( p_atk or p_spec or p_str or p_dh ) then
					self:SetWindow( DSPEC_W4_IDX )
				elseif ( w == DSPEC_W3_IDX and wt >= wl - 1 ) then
					self:SetWindow( DSPEC_W3_IDX )
				end
			end
		end

	elseif ( Attack == ERivalsCharacterAttack.Uair ) then
		if ( self:IsInputActionDown( ERivalsBufferedInputAction.Attack, true, false ) ) then
			local v = self:GetVelocity2D()
			if ( v.Y < -2.0 ) then
				self:SetVelocityVertical( -2.0 )
			end
		end

	elseif ( Attack == ERivalsCharacterAttack.Jab ) then
		Hodan2.UpdateJabLoop( self )
		if ( self:GetNetPropBoolean( JabCancel )
				and self:GetInputHistory():GetActionPressed( ERivalsBufferedInputAction.Attack ) ) then
			self:EndAttackNaturally()
		end

	elseif ( Attack == ERivalsCharacterAttack.Nair ) then
		if ( self:GetWindow() == 1 ) then
			local wt = self:GetWindowTimer()
			local held = self:IsInputActionDown( ERivalsBufferedInputAction.Attack, true, false )
			if ( wt >= 12 and held ) then
				if ( wt >= 39 ) then
					self:Lua_SetWindowTimer( 12 )
				end
			elseif ( wt >= 12 and wt < 28 ) then
				self:Lua_SetWindowTimer( 28 )
			end
		end

		if ( self:GetNetPropBoolean( NairJc )
				and self:IsInputActionDown( ERivalsBufferedInputAction.Jump, true, true ) ) then
			self:EndAttackNaturally()
		end
	end

	return true
end

function Hodan2:UpdateJabLoop()
	if ( self:GetWindow() ~= JAB_LOOP_WINDOW ) then return end
	if ( self:GetInputHistory():GetActionPressed( ERivalsBufferedInputAction.Attack ) ) then
		self:SetNetPropBoolean( JabLoopArmed, true )
	end
	if ( self:GetWindowTimer() >= ( self:GetWindowLength() - 1 )
			and self:GetNetPropBoolean( JabLoopArmed ) ) then
		self:SetNetPropBoolean( JabLoopArmed, false )
		self:SetWindow( JAB_LOOP_WINDOW )
	end
end
