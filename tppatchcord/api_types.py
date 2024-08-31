from enum import Enum
from typing import Any

from recordclass import dataobject


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

class InteractionType(int, Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

class SubscriptionStatus(int, Enum):
    ACTIVE = 0
    ENDING = 1
    INACTIVE = 2

class AuditLogEvent(int, Enum):
    GUILD_UPDATE = 1
    CHANNEL_CREATE = 10
    CHANNEL_UPDATE = 11
    CHANNEL_DELETE = 12
    CHANNEL_OVERWRITE_CREATE = 13
    CHANNEL_OVERWRITE_UPDATE = 14
    CHANNEL_OVERWRITE_DELETE = 15
    MEMBER_KICK = 20
    MEMBER_PRUNE = 21
    MEMBER_BAN_ADD = 22
    MEMBER_BAN_REMOVE = 23
    MEMBER_UPDATE = 24
    MEMBER_ROLE_UPDATE = 25
    MEMBER_MOVE = 26
    MEMBER_DISCONNECT = 27
    BOT_ADD = 28
    ROLE_CREATE = 30
    ROLE_UPDATE = 31
    ROLE_DELETE = 32
    INVITE_CREATE = 40
    INVITE_UPDATE = 41
    INVITE_DELETE = 42
    WEBHOOK_CREATE = 50
    WEBHOOK_UPDATE = 51
    WEBHOOK_DELETE = 52
    EMOJI_CREATE = 60
    EMOJI_UPDATE = 61
    EMOJI_DELETE = 62
    MESSAGE_DELETE = 72
    MESSAGE_BULK_DELETE = 73
    MESSAGE_PIN = 74
    MESSAGE_UNPIN = 75
    INTEGRATION_CREATE = 80
    INTEGRATION_UPDATE = 81
    INTEGRATION_DELETE = 82
    STAGE_INSTANCE_CREATE = 83
    STAGE_INSTANCE_UPDATE = 84
    STAGE_INSTANCE_DELETE = 85
    STICKER_CREATE = 90
    STICKER_UPDATE = 91
    STICKER_DELETE = 92
    GUILD_SCHEDULED_EVENT_CREATE = 100
    GUILD_SCHEDULED_EVENT_UPDATE = 101
    GUILD_SCHEDULED_EVENT_DELETE = 102
    THREAD_CREATE = 110
    THREAD_UPDATE = 111
    THREAD_DELETE = 112
    APPLICATION_COMMAND_PERMISSION_UPDATE = 121
    AUTO_MODERATION_RULE_CREATE = 140
    AUTO_MODERATION_RULE_UPDATE = 141
    AUTO_MODERATION_RULE_DELETE = 142
    AUTO_MODERATION_BLOCK_MESSAGE = 143
    AUTO_MODERATION_FLAG_TO_CHANNEL = 144
    AUTO_MODERATION_USER_COMMUNICATION_DISABLED = 145
    CREATOR_MONETIZATION_REQUEST_CREATED = 150
    CREATOR_MONETIZATION_TERMS_ACCEPTED = 151
    ONBOARDING_PROMPT_CREATE = 163
    ONBOARDING_PROMPT_UPDATE = 164
    ONBOARDING_PROMPT_DELETE = 165
    ONBOARDING_CREATE = 166
    ONBOARDING_UPDATE = 167
    HOME_SETTINGS_CREATE = 190
    HOME_SETTINGS_UPDATE = 191

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
    joined_at: str
    premium_since: str
    deaf: bool
    mute: bool
    flags: int
    pending: bool
    permissions: str
    communication_disabled_until: str
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
    archive_timestamp: str
    locked: bool
    invitable: bool
    create_timestamp: str

class ThreadMember(dataobject):
    id: int
    user_id: int
    join_timestamp: str
    flags: int
    member: GuildMember

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
    last_pin_timestamp: str
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

class UnavailableGuild(dataobject):
    id: int
    unavailable: bool = True

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

class IntegrationAccount(dataobject):
    id: str
    name: str

class IntegrationApplication(dataobject):
    id: int
    name: str
    icon: str
    description: str
    bot: User

class Integration(dataobject):
    id: int
    name: str
    type: str
    enabled: bool
    syncing: bool
    role_id: int
    enable_emoticons: bool
    expire_behaviour: int
    expire_grace_period: int
    user: User
    account: IntegrationAccount
    synced_at: str
    subscriber_count: int
    revoked: bool
    application: IntegrationApplication
    scopes: list[str]

class ChannelMention(dataobject):
    id: int
    guild_id: int
    type: int
    name: str

class ReactionCountDetails(dataobject):
    burst: int
    normal: int

class Reaction(dataobject):
    count: int
    count_details: ReactionCountDetails
    me: bool
    me_burst: bool
    emoji: Emoji
    burst_colors: list[str]

class EmbedThumbnail(dataobject):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedVideo(dataobject):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedImage(dataobject):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedProvider(dataobject):
    name: str
    url: str

class EmbedAuthor(dataobject):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str

class EmbedFooter(dataobject):
    text: str
    icon_url: str
    proxy_icon_url: str

class EmbedField(dataobject):
    name: str
    value: str
    inline: bool

class Embed(dataobject):
    title: str
    type: str
    description: str
    url: str
    timestamp: str
    color: int
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedProvider
    author: EmbedAuthor
    fields: list[EmbedField]

class Attachment(dataobject):
    id: int
    filename: str
    title: str
    description: str
    content_type: str
    size: int
    url: str
    proxy_url: str
    height: int
    width: int
    ephemeral: bool
    duration_secs: float
    waveform: str
    flags: int

class MessageActivity(dataobject):
    type: int
    party_id: str

class MessageReference(dataobject):
    type: int
    message_id: int
    channel_id: int
    guild_id: int
    fail_if_not_exists: bool

class MessageSnapshotPartialMessage(dataobject):
    type: int
    content: str
    embeds: list[Embed]
    attachments: list[Attachment]
    timestamp: str
    edited_timestamp: str
    flags: int
    mentions: list[User]
    mention_roles: list[Role]

class MessageSnapshot(dataobject):
    message: MessageSnapshotPartialMessage

class MessageInteractionMetadata(dataobject):
    id: int
    interaction: InteractionType
    user: User
    authorizing_integration_owners: dict
    original_response_message_id: int
    interacted_message_id: int
    triggering_interaction_metadata: "MessageInteractionMetadata"

class MessageInteraction(dataobject):
    id: int
    type: InteractionType
    name: str
    user: User
    member: GuildMember

class MessageStickerItem(dataobject):
    id: int
    name: str
    format_type: int

class RoleSubscriptionData(dataobject):
    role_subscription_listing_id: int
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool

class Resolved(dataobject):
    users: dict[int, User]
    members: dict[int, GuildMember]
    roles: dict[int, Role]
    channels: dict[int, Channel]
    messages: dict[int, "Message"]
    attachments: dict[int, Attachment]

class PollMedia(dataobject):
    text: str
    emoji: Emoji

class PollAnswer(dataobject):
    answer_id: int
    poll_media: PollMedia

class PollAnswerCount(dataobject):
    id: int
    count: int
    me_voted: bool

class PollResults(dataobject):
    is_finalized: bool
    answer_counts: list[PollAnswerCount]

class Poll(dataobject):
    question: PollMedia
    answer: list[PollAnswer]
    expiry: str
    allow_multiselect: bool
    layout_type: int
    results: PollResults

class MessageCall(dataobject):
    participants: list[int]
    ended_timestamp: str

class Component(dataobject):
    ...

class Message(dataobject):
    id: int
    channel_id: int
    author: User
    content: str
    timestamp: str
    edited_timestamp: str
    tts: bool
    mention_everyone: bool
    mentions: list[User]
    mention_roles: list[Role]
    mention_channels: list[ChannelMention]
    attachments: list[Attachment]
    embeds: list[Embed]
    reactions: list[Reaction]
    nonce: int | str
    pinned: bool
    webhook_id: int
    type: int
    activity: MessageActivity
    application: Application
    application_id: int
    flags: int
    message_reference: MessageReference
    message_snapshots: list[MessageSnapshot]
    referenced_message: "Message"
    interaction_metadata: MessageInteractionMetadata
    interaction: MessageInteraction
    thread: Channel
    components: list[Component] # FIXME(idmp152): RETURNS A DICT NOW!!! https://discord.com/developers/docs/interactions/message-components#component-object NOT YET IMPLEMENTED
    sticker_items: list[MessageStickerItem]
    stickers: list[Sticker]
    position: int
    role_subscription_data: RoleSubscriptionData
    resolved: Resolved
    poll: Poll
    call: MessageCall

class Subscription(dataobject):
    id: int
    user_id: int
    sku_ids: list[int]
    entitlement_ids: list[int]
    current_period_start: str
    current_period_end: str
    status: SubscriptionStatus
    canceled_at: str
    country: str

class AuditLogChange(dataobject):
    new_value: Any
    old_value: Any
    key: str

class OptionalAuditEntryInfo(dataobject):
    application_id: int
    auto_moderation_rule_name: str
    auto_moderation_rule_trigger_type: str
    channel_id: int
    count: str
    delete_member_days: str
    id: int
    members_removed: str
    message_id: int
    role_name: str
    type: str
    integration_type: str

class AuditLogEntry(dataobject):
    target_id: str
    changes: list[AuditLogChange]
    user_id: int
    id: int
    action_type: AuditLogEvent
    options: OptionalAuditEntryInfo
    reason: str

class Hello(EventData):
    heartbeat_interval: int

class Ready(EventData):
    v: int
    user: User
    guilds: list[UnavailableGuild]
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

class IntegrationDelete(EventData):
    id: int
    guild_id: int
    application_id: int

class InviteCreate(EventData):
    channel_id: int
    code: str
    created_at: str
    guild_id: int
    inviter: User
    max_age: int
    max_uses: int
    target_type: int
    target_user: User
    target_application: Application
    temporary: bool
    uses: int

class InviteDelete(EventData):
    channel_id: int
    guild_id: int
    code: str

class MessageDelete(EventData):
    id: int
    channel_id: int
    guild_id: int

class MessageDeleteBulk(EventData):
    id: int
    channel_id: int
    guild_id: int


class MessageReactionAdd(EventData):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    member: GuildMember
    emoji: Emoji
    message_author_id: int
    burst: bool
    burst_colors: list[str]
    type: int

class MessageReactionRemove(EventData):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    emoji: Emoji
    burst: bool
    type: int

class MessageReactionRemoveAll(EventData):
    channel_id: int
    message_id: int
    guild_id: int

class MessageReactionRemoveEmoji(EventData):
    channel_id: int
    guild_id: int
    message_id: int
    emoji: Emoji

class PresenceUpdate(EventData):
    user: User
    guild_id: int
    status: str
    activities: list[Activity]
    client_status: ClientStatus

class TypingStart(EventData):
    channel_id: int
    guild_id: int
    user_id: int
    timestamp: int
    member: GuildMember

class VoiceChannelEffectSend(EventData):
    channel_id: int
    guild_id: int
    user_id: int
    emoji: Emoji
    animation_type: int
    animation_id: int
    sound_id: int
    sound_volume: float

class VoiceServerUpdate(EventData):
    token: str
    guild_id: int
    endpoint: str

class WebhooksUpdate(EventData):
    guild_id: int
    channel_id: int

class MessagePollVoteAdd(EventData):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    answer_id: int
    
class MessagePollVoteRemove(EventData):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    answer_id: int

class ThreadCreate(Channel, EventData):
    newly_created: bool

class IntegrationCreate(Integration, EventData):
    guild_id: int

class IntegrationUpdate(Integration, EventData):
    guild_id: int

class ThreadMemberUpdate(ThreadMember, EventData):
    guild_id: int

class ThreadMembersUpdate(EventData):
    id: int
    guild_id: int
    member_count: int
    added_members: list[ThreadMember]
    removed_member_ids: list[int]

class MessageCreate(Message, EventData):
    guild_id: int
    member: GuildMember
    # mentions: list[User] 

class MessageUpdate(Message, EventData):
    guild_id: int
    member: GuildMember
    # mentions: list[User]

class GuildCreate(Guild, EventData):
    joined_at: str
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

class GuildAuditLogEntryCreate(AuditLogEntry, EventData):
    guild_id: int

class GuildBanAdd(EventData):
    guild_id: int
    user: User

class GuildBanRemove(EventData):
    guild_id: int
    user: User

class GuildEmojisUpdate(EventData):
    guild_id: int
    emojis: list[Emoji]

class GuildStickersUpdate(EventData):
    guild_id: int
    stickers: list[Sticker]

class GuildIntegrationsUpdate(EventData):
    guild_id: int

class GuildMemberAdd(GuildMember, EventData):
    guild_id: int

class GuildMemberRemove(EventData):
    guild_id: int
    user: User

class GuildMemberUpdate(EventData):
    guild_id: int
    roles: list[int]
    user: User
    nick: str
    avatar: str
    joined_at: str
    premium_since: str
    deaf: bool
    mute: bool
    pending: bool
    communication_disabled_until: str
    flags: int
    avatar_decoration_data: AvatarDecorationData

class GuildMembersChunk(EventData):
    guild_id: int
    members: list[GuildMember]
    chunk_index: int
    chunk_count: int
    not_found: list
    presences: list[PresenceUpdate]
    nonce: str

class GuildRoleCreate(EventData):
    guild_id: int
    role: Role

class GuildRoleUpdate(EventData):
    guild_id: int
    role: Role

class GuildRoleDelete(EventData):
    guild_id: int
    role: Role

class Event(dataobject):
    opcode: int
    sequence: int
    name: str
    data: EventData | dataobject | bool | None


#TODO(idmp152): Document classes in format:
"""This is a test class for dataclasses.

    This is the body of the docstring description.

    Args:
        var_int (int): An integer.
        var_str (str): A string.

    """