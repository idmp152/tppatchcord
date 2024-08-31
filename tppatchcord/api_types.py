import sys

from enum import Enum
from typing import Any, get_args, get_origin
from types import UnionType
import logging

from recordclass import dataobject


logging.basicConfig(format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

class InteractionContextType(int, Enum):
    GUILD = 0
    BOT_DM = 1
    PRIVATE_CHANNEL = 2

class Serializable(dataobject):
    @classmethod
    def from_dict(cls, payload: dict) -> "Serializable":
        obj = cls()
        for key, value in payload.items():
            if key in obj.__fields__:
                setattr(obj, key, value) # REMOVES EXCESSIVE DATA GIVEN BY THE API. EITHER DOCUMENT IT, OR DON'T GIVE IT TO THE USER, DISCORD!!!! #rant
            else:
                logger.warning("Field %s ignored when serializing %s", key, cls)
        
        for field_name, typeclass in cls.__annotations__.items():
            annot_type = typeclass

            # handle self-references through string annotations
            if isinstance(annot_type, str):
                annot_type = getattr(sys.modules[__name__], annot_type)

            # handle generic["String"] self-references with annotations
            annot_type_args = list(get_args(annot_type))
            for i in range(len((annot_type_args))):
                if isinstance(annot_type_args[i], str):
                    annot_type_args[i] = getattr(sys.modules[__name__], annot_type_args[i])

            field = getattr(obj, field_name)
            if field:
                if isinstance(annot_type, UnionType):
                    continue
                # handle field: list[Serializable]
                elif get_origin(annot_type) is list and annot_type_args and issubclass(annot_type_args[0], Serializable):
                    for i in range(len(field)):
                        field[i] = get_args(annot_type)[0].from_dict(field[i])

                # handle field: dict[x, Serializable]
                elif get_origin(annot_type) is dict and annot_type_args and issubclass(annot_type_args[1], Serializable):
                    for k in field:
                        field[k] = get_args(annot_type)[1].from_dict(field[k])

                elif issubclass(annot_type, Serializable):
                    setattr(obj, field_name, annot_type.from_dict(field))

        return obj


class AvatarDecorationData(Serializable):
    asset: str
    sku_id: int

class User(Serializable):
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
    clan: Any # UNDOCUMENTED FIELD IN THE API!!! BUT STILL RETURNED!! #rant
    
class RoleTags(Serializable):
    bot_id: int
    integration_id: int
    premium_subscriber: bool
    subscription_listing_id: int
    available_for_purchase: bool
    guild_connections: bool

class Role(Serializable):
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

class Emoji(Serializable):
    id: int
    name: str
    roles: list[Role]
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool

class WelcomeScreenChannel(Serializable):
    channel_id: int
    description: str
    emoji_id: int
    emoji_name: str

class WelcomeScreen(Serializable):
    description: str
    welcome_channels: list[WelcomeScreenChannel]

class Sticker(Serializable):
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

class GuildMember(Serializable):
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
    banner: str # UNDOCUMENTED FIELD IN THE API!!! BUT STILL RETURNED!! #rant

class Application(Serializable):
    ...

class ActionMetadata(Serializable):
    channel_id: int
    duration_seconds: int
    custom_message: str

class AutoModerationAction(Serializable):
    type: ActionType
    metadata: ActionMetadata

class TriggerMetadata(Serializable):
    keyword_filter: list[str]
    regex_patterns: list[str]
    presets: list[KeywordPresetType]
    allow_list: list[str]
    mention_total_limit: int
    mention_raid_protection_enabled: bool

class AutoModerationRule(Serializable):
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

class Overwrite(Serializable):
    id: int
    type: int
    allow: str
    deny: str

class ThreadMetadata(Serializable):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: bool
    create_timestamp: str

class ThreadMember(Serializable):
    id: int
    user_id: int
    join_timestamp: str
    flags: int
    member: GuildMember

class ForumTag(Serializable):
    id: int
    name: str
    moderated: bool
    emoji_id: int
    emoji_name: str

class DefaultReaction(Serializable):
    emoji_id: int
    emoji_name: str

class Channel(Serializable):
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

class Entitlement(Serializable):
    id: int
    sku_id: int
    application_id: int
    user_id: int
    type: int
    deleted: bool
    starts_at: str
    ends_at: str
    guild_id: int
    consumed: bool

class VoiceState(Serializable):
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

class ClientStatus(Serializable):
    desktop: str
    mobile: str
    web: str

class ActivityParty(Serializable):
    id: int
    size: list[int, int]

class ActivityAssets(Serializable):
    large_image: str
    large_text: str
    small_image: str
    small_text: str

class ActivitySecrets(Serializable):
    join: str
    spectate: str
    match: str

class ActivityTimestamps(Serializable):
    start: int
    end: int

class ActivityButton(Serializable):
    label: str
    url: str

class Activity(Serializable):
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

class StageInstance(Serializable):
    id: int
    guild_id: int
    channel_id: int
    topic: str
    privacy_level: int
    discoverable_disabled: bool
    guild_scheduled_event_id: int

class GuildScheduledEventEntityMetadata(Serializable):
    location: str

class RecurrenceNWeekday(Serializable):
    n: int
    day: int

class GuildScheduledEventRecurrenceRule(Serializable):
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

class GuildScheduledEvent(Serializable):
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

class UnavailableGuild(Serializable):
    id: int
    unavailable: bool = True

class Guild(Serializable):
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
    unavailable: bool = False

class IntegrationAccount(Serializable):
    id: str
    name: str

class IntegrationApplication(Serializable):
    id: int
    name: str
    icon: str
    description: str
    bot: User

class Integration(Serializable):
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

class ChannelMention(Serializable):
    id: int
    guild_id: int
    type: int
    name: str

class ReactionCountDetails(Serializable):
    burst: int
    normal: int

class Reaction(Serializable):
    count: int
    count_details: ReactionCountDetails
    me: bool
    me_burst: bool
    emoji: Emoji
    burst_colors: list[str]

class EmbedThumbnail(Serializable):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedVideo(Serializable):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedImage(Serializable):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedProvider(Serializable):
    name: str
    url: str

class EmbedAuthor(Serializable):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str

class EmbedFooter(Serializable):
    text: str
    icon_url: str
    proxy_icon_url: str

class EmbedField(Serializable):
    name: str
    value: str
    inline: bool

class Embed(Serializable):
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

class Attachment(Serializable):
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

class MessageActivity(Serializable):
    type: int
    party_id: str

class MessageReference(Serializable):
    type: int
    message_id: int
    channel_id: int
    guild_id: int
    fail_if_not_exists: bool

class MessageSnapshotPartialMessage(Serializable):
    type: int
    content: str
    embeds: list[Embed]
    attachments: list[Attachment]
    timestamp: str
    edited_timestamp: str
    flags: int
    mentions: list[User]
    mention_roles: list[Role]

class MessageSnapshot(Serializable):
    message: MessageSnapshotPartialMessage

class MessageInteractionMetadata(Serializable):
    id: int
    interaction: InteractionType
    user: User
    authorizing_integration_owners: dict
    original_response_message_id: int
    interacted_message_id: int
    triggering_interaction_metadata: "MessageInteractionMetadata"

class MessageInteraction(Serializable):
    id: int
    type: InteractionType
    name: str
    user: User
    member: GuildMember

class MessageStickerItem(Serializable):
    id: int
    name: str
    format_type: int

class RoleSubscriptionData(Serializable):
    role_subscription_listing_id: int
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool

class Resolved(Serializable):
    users: dict[int, User]
    members: dict[int, GuildMember]
    roles: dict[int, Role]
    channels: dict[int, Channel]
    messages: dict[int, "Message"]
    attachments: dict[int, Attachment]

class PollMedia(Serializable):
    text: str
    emoji: Emoji

class PollAnswer(Serializable):
    answer_id: int
    poll_media: PollMedia

class PollAnswerCount(Serializable):
    id: int
    count: int
    me_voted: bool

class PollResults(Serializable):
    is_finalized: bool
    answer_counts: list[PollAnswerCount]

class Poll(Serializable):
    question: PollMedia
    answer: list[PollAnswer]
    expiry: str
    allow_multiselect: bool
    layout_type: int
    results: PollResults

class MessageCall(Serializable):
    participants: list[int]
    ended_timestamp: str

class Component(Serializable):
    # TEMPORARY, NOT IMPLEMENTED, SEE TODOS
    @classmethod
    def from_dict(cls, payload: dict) -> Serializable:
        return payload

class Message(Serializable):
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
    components: list[Component] # FIXME(idmp152): RETURNS A DICT FOR NOW!!! https://discord.com/developers/docs/interactions/message-components#component-object NOT YET IMPLEMENTED
    sticker_items: list[MessageStickerItem]
    stickers: list[Sticker]
    position: int
    role_subscription_data: RoleSubscriptionData
    resolved: Resolved
    poll: Poll
    call: MessageCall

class Subscription(Serializable):
    id: int
    user_id: int
    sku_ids: list[int]
    entitlement_ids: list[int]
    current_period_start: str
    current_period_end: str
    status: SubscriptionStatus
    canceled_at: str
    country: str

class AuditLogChange(Serializable):
    new_value: Any
    old_value: Any
    key: str

class OptionalAuditEntryInfo(Serializable):
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

class AuditLogEntry(Serializable):
    target_id: str
    changes: list[AuditLogChange]
    user_id: int
    id: int
    action_type: AuditLogEvent
    options: OptionalAuditEntryInfo
    reason: str

class ApplicationCommandInteractionDataOption(Serializable):
    name: str
    type: int
    value: str | int | float | bool
    options: list["ApplicationCommandInteractionDataOption"]
    focused: bool

class SelectOption(Serializable):
    label: str
    value: str
    description: str
    emoji: Emoji
    default: bool

class InteractionData(Serializable):
    # Application Command Data
    id: int
    name: str
    type: int
    resolved: Resolved
    options: list[ApplicationCommandInteractionDataOption]
    guild_id: int
    target_id: int
    # Message Component Data
    custom_id: str
    component_type: int
    values: list[SelectOption]
    # Modal Submit Data
    components: list[Component]

class Interaction(Serializable):
    id: int
    application_id: int
    type: InteractionType
    data: InteractionData
    guild: Guild
    guild_id: int
    channel: Channel
    channel_id: int
    member: GuildMember
    user: User
    token: str
    version: int
    message: Message
    app_permissions: str
    locale: str
    guild_locale: str 
    entitlements: list[Entitlement]
    authorizing_integration_owners: dict
    context: InteractionContextType

class Hello(Serializable):
    heartbeat_interval: int

class Ready(Serializable):
    v: int
    user: User
    guilds: list[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: list[int, int]
    application: Application

    @classmethod
    def from_dict(cls, payload: dict) -> Serializable: # TODO(idmp152): Fix READY event serialization (check additional undocumented fields)
        return payload

class ApplicationCommandPermissions(Serializable):
    id: int
    type: ApplicationCommandPermissionType
    permission: bool

class AutoModerationActionExecution(Serializable):
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

class ThreadListSync(Serializable):
    guild_id: int
    channel_ids: list[int]
    threads: list[Channel]
    members: list[ThreadMember]

class ChannelPinsUpdate(Serializable):
    guild_id: int
    channel_id: int
    last_pin_timestamp: int

class IntegrationDelete(Serializable):
    id: int
    guild_id: int
    application_id: int

class InviteCreate(Serializable):
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

class InviteDelete(Serializable):
    channel_id: int
    guild_id: int
    code: str

class MessageDelete(Serializable):
    id: int
    channel_id: int
    guild_id: int

class MessageDeleteBulk(Serializable):
    id: int
    channel_id: int
    guild_id: int


class MessageReactionAdd(Serializable):
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

class MessageReactionRemove(Serializable):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    emoji: Emoji
    burst: bool
    type: int

class MessageReactionRemoveAll(Serializable):
    channel_id: int
    message_id: int
    guild_id: int

class MessageReactionRemoveEmoji(Serializable):
    channel_id: int
    guild_id: int
    message_id: int
    emoji: Emoji

class PresenceUpdate(Serializable):
    user: User
    guild_id: int
    status: str
    activities: list[Activity]
    client_status: ClientStatus

class TypingStart(Serializable):
    channel_id: int
    guild_id: int
    user_id: int
    timestamp: int
    member: GuildMember

class VoiceChannelEffectSend(Serializable):
    channel_id: int
    guild_id: int
    user_id: int
    emoji: Emoji
    animation_type: int
    animation_id: int
    sound_id: int
    sound_volume: float

class VoiceServerUpdate(Serializable):
    token: str
    guild_id: int
    endpoint: str

class WebhooksUpdate(Serializable):
    guild_id: int
    channel_id: int

class MessagePollVoteAdd(Serializable):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    answer_id: int
    
class MessagePollVoteRemove(Serializable):
    user_id: int
    channel_id: int
    message_id: int
    guild_id: int
    answer_id: int

class ThreadCreate(Channel):
    newly_created: bool

class IntegrationCreate(Integration):
    guild_id: int

class IntegrationUpdate(Integration):
    guild_id: int

class ThreadMemberUpdate(ThreadMember):
    guild_id: int

class ThreadMembersUpdate(Serializable):
    id: int
    guild_id: int
    member_count: int
    added_members: list[ThreadMember]
    removed_member_ids: list[int]

class MessageCreate(Message):
    guild_id: int
    member: GuildMember
    # mentions: list[User] 

class MessageUpdate(Message):
    guild_id: int
    member: GuildMember
    # mentions: list[User]

class GuildCreate(Guild):
    joined_at: str
    large: bool
    member_count: int
    voice_states: list[VoiceState]
    members: list[GuildMember]
    channels: list[Channel]
    threads: list[Channel]
    presences: list[PresenceUpdate]
    stage_instances: list[StageInstance]
    guild_scheduled_events: list[GuildScheduledEvent]

class GuildAuditLogEntryCreate(AuditLogEntry):
    guild_id: int

class GuildBanAdd(Serializable):
    guild_id: int
    user: User

class GuildBanRemove(Serializable):
    guild_id: int
    user: User

class GuildEmojisUpdate(Serializable):
    guild_id: int
    emojis: list[Emoji]

class GuildStickersUpdate(Serializable):
    guild_id: int
    stickers: list[Sticker]

class GuildIntegrationsUpdate(Serializable):
    guild_id: int

class GuildMemberAdd(GuildMember):
    guild_id: int

class GuildMemberRemove(Serializable):
    guild_id: int
    user: User

class GuildMemberUpdate(Serializable):
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

class GuildMembersChunk(Serializable):
    guild_id: int
    members: list[GuildMember]
    chunk_index: int
    chunk_count: int
    not_found: list
    presences: list[PresenceUpdate]
    nonce: str

class GuildRoleCreate(Serializable):
    guild_id: int
    role: Role

class GuildRoleUpdate(Serializable):
    guild_id: int
    role: Role

class GuildRoleDelete(Serializable):
    guild_id: int
    role: Role

class GuildScheduledEventUserAdd(Serializable):
    guild_scheduled_event_id: int
    user_id: int
    guild_id: int

class GuildScheduledEventUserRemove(Serializable):
    guild_scheduled_event_id: int
    user_id: int
    guild_id: int

class Event(dataobject):
    opcode: int
    sequence: int
    name: str
    data: Serializable | bool | None


EVENT_DATAOBJECTS = {
    "HELLO": Hello,
    "READY": Ready,
    "APPLICATION_COMMAND_PERMISSIONS_UPDATE": ApplicationCommandPermissions,
    "AUTO_MODERATION_RULE_CREATE": AutoModerationRule,
    "AUTO_MODERATION_RULE_UPDATE": AutoModerationRule,
    "AUTO_MODERATION_RULE_DELETE": AutoModerationRule,
    "AUTO_MODERATION_ACTION_EXECUTION": AutoModerationActionExecution,
    "CHANNEL_CREATE": Channel,
    "CHANNEL_UPDATE": Channel,
    "CHANNEL_DELETE": Channel,
    "THREAD_CREATE": ThreadCreate,
    "THREAD_UPDATE": Channel,
    "THREAD_DELETE": Channel,
    "THREAD_LIST_SYNC": ThreadListSync,
    "THREAD_MEMBER_UPDATE": ThreadMemberUpdate,
    "THREAD_MEMBERS_UPDATE": ThreadMembersUpdate,
    "CHANNEL_PINS_UPDATE": ChannelPinsUpdate,
    "ENTITLEMENT_CREATE": Entitlement,
    "ENTITLEMENT_UPDATE": Entitlement,
    "ENTITLEMENT_DELETE": Entitlement,
    "GUILD_CREATE": GuildCreate,
    "GUILD_UPDATE": Guild,
    "GUILD_DELETE": UnavailableGuild,
    "GUILD_AUDIT_LOG_ENTRY_CREATE": GuildAuditLogEntryCreate,
    "GUILD_BAN_ADD": GuildBanAdd,
    "GUILD_BAN_REMOVE": GuildBanRemove,
    "GUILD_EMOJIS_UPDATE": GuildEmojisUpdate,
    "GUILD_STICKERS_UPDATE": GuildStickersUpdate,
    "GUILD_INTEGRATIONS_UPDATE": GuildIntegrationsUpdate,
    "GUILD_MEMBER_ADD": GuildMemberAdd,
    "GUILD_MEMBER_REMOVE": GuildMemberRemove,
    "GUILD_MEMBER_UPDATE": GuildMemberUpdate,
    "GUILD_MEMBERS_CHUNK": GuildMembersChunk,
    "GUILD_ROLE_CREATE": GuildRoleCreate,
    "GUILD_ROLE_UPDATE": GuildRoleUpdate,
    "GUILD_ROLE_DELETE": GuildRoleDelete,
    "GUILD_SCHEDULED_EVENT_CREATE": GuildScheduledEvent,
    "GUILD_SCHEDULED_EVENT_UPDATE": GuildScheduledEvent,
    "GUILD_SCHEDULED_EVENT_DELETE": GuildScheduledEvent,
    "GUILD_SCHEDULED_EVENT_USER_ADD": GuildScheduledEventUserAdd,
    "GUILD_SCHEDULED_EVENT_USER_REMOVE": GuildScheduledEventUserRemove,
    "INTEGRATION_CREATE": IntegrationCreate,
    "INTEGRATION_UPDATE": IntegrationUpdate,
    "INTEGRATION_DELETE": IntegrationDelete,
    "INVITE_CREATE": InviteCreate,
    "INVITE_DELETE": InviteDelete,
    "MESSAGE_CREATE": MessageCreate,
    "MESSAGE_UPDATE": MessageUpdate,
    "MESSAGE_DELETE": MessageDelete,
    "MESSAGE_DELETE_BULK": MessageDeleteBulk,
    "MESSAGE_REACTION_ADD": MessageReactionAdd,
    "MESSAGE_REACTION_REMOVE": MessageReactionRemove,
    "MESSAGE_REACTION_REMOVE_ALL": MessageReactionRemoveAll,
    "MESSAGE_REACTION_REMOVE_EMOJI": MessageReactionRemoveEmoji,
    "PRESENCE_UPDATE": PresenceUpdate,
    "TYPING_START": TypingStart,
    "VOICE_CHANNEL_EFFECT_SEND": VoiceChannelEffectSend,
    "VOICE_STATE_UPDATE": VoiceState,
    "VOICE_SERVER_UPDATE": VoiceServerUpdate,
    "WEBHOOKS_UPDATE": WebhooksUpdate,
    "INTERACTION_CREATE": Interaction,
    "STAGE_INSTANCE_CREATE": StageInstance,
    "STAGE_INSTANCE_UPDATE": StageInstance,
    "STAGE_INSTANCE_DELETE": StageInstance,
    "SUBSCRIPTION_CREATE": Subscription,
    "SUBSCRIPTION_UPDATE": Subscription,
    "SUBSCRIPTION_DELETE": Subscription,
    "MESSAGE_POLL_VOTE_ADD": MessagePollVoteAdd,
    "MESSAGE_POLL_VOTE_REMOVE": MessagePollVoteRemove
}

def process_event_payload(payload: dict) -> Event:
    """
    Preprocess raw JSON data into a dataclass-like object. (api_types.py)
    Uses recordclass.dataobject type for higher performance, inheritance and low memory footprint

    :param payload: payload
    :returns: Dataclass-like Discord API stuct
    """

    event = Event(opcode=payload["op"], sequence=payload["s"], name=payload["t"])
    event_dataobject = EVENT_DATAOBJECTS.get(event.name)
    event.data = event_dataobject.from_dict(payload["d"]) if event_dataobject else payload["d"]
    return event

#TODO(idmp152): Document classes in format:
"""This is a test class for dataclasses.

    This is the body of the docstring description.

    Args:
        var_int (int): An integer.
        var_str (str): A string.

    """

#TODO(idmp152): replace int and str types for snowflake ids and timestapms with typing.NewType (possibly)