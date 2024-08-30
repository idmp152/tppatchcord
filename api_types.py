from typing import Any
from recordclass import dataobject
from enum import Enum

class ApplicationCommandPermissionType(int, Enum):
    ROLE = 1
    USER = 2
    CHANNEL = 3

class KeywordPresetType(int, Enum):
    PROFANITY = 1
    SEXUAL_CONTENT = 2
    SLURS = 3

class EventType(int, Enum):
    MESSAGE_SEND = 1
    MEMBER_UPDATE = 2

class TriggerType(int, Enum):
    KEYWORD = 1
    SPAM = 2
    KEYWORD_PRESET = 3
    MENTION_SPAM = 4
    MEMBER_PROFILE = 5

class ActionType(int, Enum):
    BLOCK_MESSAGE = 1
    SEND_ALERT_MESSAGE = 2
    TIMEOUT = 3
    BLOCK_MEMBER_INTERACTION = 4

class ChannelType(int, Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15
    GUILD_MEDIA = 16

class EventData(dataobject):
    ...

class AvatarDecorationData(dataobject):
    asset: str
    sku_id: int

class User(dataobject):
    id: int
    username: str
    discriminator: str
    global_name: str
    avatar: str
    bot: bool
    system: bool
    mfa_enabled: bool
    banner: str
    accent_color: int
    locale: str
    verified: bool
    email: str
    flags: int
    premium_type: int
    public_flags: int
    avatar_decoration_data: AvatarDecorationData
    
class RoleTags(dataobject):
    bot_id: int
    integration_id: int
    premium_subscriber: bool
    subscription_listing_id: int
    available_for_purchase: bool
    guild_connections: bool

class Role(dataobject):
    id: int
    name: str
    color: int
    hoist: bool
    icon: bool
    unicode_emoji: str
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: RoleTags
    flags: int

class Emoji(dataobject):
    id: int
    name: str
    roles: list[Role]
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool

class WelcomeScreenChannel(dataobject):
    channel_id: int
    description: str
    emoji_id: int
    emoji_name: str

class WelcomeScreen(dataobject):
    description: str
    welcome_channels: list[WelcomeScreenChannel]

class Sticker(dataobject):
    id: int
    pack_id: int
    name: str
    description: str
    tags: str
    asset: str
    type: int
    format_type: int
    available: bool
    guild_id: int
    user: User
    sort_value: int

class GuildMember(dataobject):
    user: User
    nick: str
    avatar: str
    roles: list[int]
    joined_at: int
    premium_since: int
    deaf: bool
    mute: bool
    flags: int
    pending: bool
    permissions: str
    communication_disabled_until: int
    avatar_decoration_data: AvatarDecorationData

class Application(dataobject):
    ...

class ActionMetadata(dataobject):
    channel_id: int
    duration_seconds: int
    custom_message: str

class AutoModerationAction(dataobject):
    type: ActionType
    metadata: ActionMetadata

class TriggerMetadata(dataobject):
    keyword_filter: list[str]
    regex_patterns: list[str]
    presets: list[KeywordPresetType]
    allow_list: list[str]
    mention_total_limit: int
    mention_raid_protection_enabled: bool

class AutoModerationRule(dataobject):
    id: int
    guild_id: int
    name: str
    creator_id: int
    event_type: EventType
    trigger_type: TriggerType
    trigger_metadata: TriggerMetadata
    actions: list[AutoModerationAction]
    enabled: bool
    exempt_rules: list[int]
    exempt_channels: list[int]

class Overwrite(dataobject):
    id: int
    type: int
    allow: str
    deny: str

class ThreadMetadata(dataobject):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: int
    locked: bool
    invitable: bool
    create_timestamp: int

class ThreadMember(dataobject):
    id: int
    user_id: int
    join_timestamp: int
    flags: int
    member: GuildMember
    # extra fields
    guild_id: int

class ForumTag(dataobject):
    id: int
    name: str
    moderated: bool
    emoji_id: int
    emoji_name: str

class DefaultReaction(dataobject):
    emoji_id: int
    emoji_name: str

class Channel(dataobject):
    id: int
    type: ChannelType
    guild_id: int
    position: int
    permission_overwrites: list[Overwrite]
    name: str
    topic: str
    nsfw: bool
    last_message_id: int
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: list[User]
    icon: str
    owner_id: int
    application_id: int
    managed: bool
    parent_id: int
    last_pin_timestamp: int
    rtc_region: str
    video_quality_mode: int
    message_count: int
    member_count: int
    thread_metadata: ThreadMetadata
    member: ThreadMember
    default_auto_archive_duration: int
    permissions: str
    flags: int
    total_message_sent: int
    available_tags: list[ForumTag]
    applied_tags: list[int]
    default_reaction_emoji: DefaultReaction
    default_thread_rate_limit_per_user: int
    default_sort_order: int
    default_forum_layout: int
    newly_created: bool

class Entitlement(dataobject):
    id: int
    sku_id: int
    application_id: int
    user_id: int
    type: int
    deleted: bool
    starts_at: int
    ends_at: int
    guild_id: int
    consumed: bool

class VoiceState(dataobject):
    guild_id: int
    channel_id: int
    user_id: int
    member: GuildMember
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: bool
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: int

class ClientStatus(dataobject):
    desktop: str
    mobile: str
    web: str

class ActivityParty(dataobject):
    id: int
    size: list[int, int]

class ActivityAssets(dataobject):
    large_image: str
    large_text: str
    small_image: str
    small_text: str

class ActivitySecrets(dataobject):
    join: str
    spectate: str
    match: str

class ActivityTimestamps(dataobject):
    start: int
    end: int

class ActivityButton(dataobject):
    label: str
    url: str

class Activity(dataobject):
    name: str
    type: int
    url: str
    created_at: int
    timestamps: ActivityTimestamps
    application_id: int
    details: str
    state: str
    emoji: Emoji
    party: ActivityParty
    assets: ActivityAssets
    secrets: ActivitySecrets 
    instance: bool
    flags: int
    buttons: list[ActivityButton]

class PresenceUpdate(EventData):
    user: User
    guild_id: int
    status: str
    activities: list[Activity]
    client_status: ClientStatus

class StageInstance(dataobject):
    id: int
    guild_id: int
    channel_id: int
    topic: str
    privacy_level: int
    discoverable_disabled: bool
    guild_scheduled_event_id: int

class GuildScheduledEventEntityMetadata(dataobject):
    location: str

class RecurrenceNWeekday(dataobject):
    n: int
    day: int

class GuildScheduledEventRecurrenceRule(dataobject):
    start: str
    end: str
    frequency: int
    interval: int
    by_weekday: list[int]
    by_n_weekday: list[RecurrenceNWeekday]
    by_month: list[int]
    by_month_day: list[int]
    by_year_day: list[int]
    count: int

class GuildScheduledEvent(dataobject):
    id: int
    guild_id: int
    channel_id: int
    creator_id: int
    name: str
    description: str
    scheduled_start_time: str
    scheduled_end_time: str
    privacy_level: int
    status: int
    entity_type: int
    entity_id: int
    entity_metadata: GuildScheduledEventEntityMetadata
    creator: User
    user_count: int
    image: str
    reccurence_rule: GuildScheduledEventRecurrenceRule

class Guild(dataobject):
    id: int
    name: str
    icon: str
    icon_hash: str
    splash: str
    discovery_splash: str
    owner: bool
    owner_id: int
    permissions: str
    region: str
    afk_channel_id: int
    afk_timeout: int
    widget_enabled: bool
    widget_channel_id: int
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: list[Role]
    emojis: list[Emoji]
    features: list[str]
    mfa_level: int
    application_id: int
    system_channel_id: int
    system_channel_flags: int
    rules_channel_id: int
    max_presences: int
    max_members: int
    vanity_url_code: str
    description: str
    banner: str
    premium_tier: int
    premium_subscription_count: int
    preferred_locale: str
    public_updates_channel_id: int
    max_video_channel_users: int
    max_stage_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: WelcomeScreen
    nsfw_level: int
    stickers: list[Sticker]
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: int
    # extra fields
    joined_at: int
    large: bool
    unavailable: bool
    member_count: int
    voice_states: list[VoiceState]
    members: list[GuildMember]
    channels: list[Channel]
    threads: list[Channel]
    presences: list[PresenceUpdate]
    stage_instances: list[StageInstance]
    guild_scheduled_events: list[GuildScheduledEvent]


class Hello(EventData):
    heartbeat_interval: int

class Ready(EventData):
    v: int
    user: User
    guilds: list[Guild]
    session_id: str
    resume_gateway_url: str
    shard: list[int, int]
    application: Application

class ApplicationCommandPermissions(EventData):
    id: int
    type: ApplicationCommandPermissionType
    permission: bool

class AutoModerationActionExecution(EventData):
    guild_id: int
    action: AutoModerationAction
    rule_id: int
    rule_trigger_type: TriggerType
    user_id: int
    channel_id: int
    message_id: int
    alert_system_message_id: int
    content: str
    matched_keyword: str
    matched_content: str

class ThreadListSync(EventData):
    guild_id: int
    channel_ids: list[int]
    threads: list[Channel]
    members: list[ThreadMember]

class ChannelPinsUpdate(EventData):
    guild_id: int
    channel_id: int
    last_pin_timestamp: int

class Event(dataobject):
    opcode: int
    sequence: int
    name: str
    data: EventData | dataobject | bool | None