# Entity Relationship Diagrams

Only the facts that cause wrong or unrenderable ERDs. Basic `erDiagram` syntax is assumed known.

## Schema to diagram

1. List entities (tables). Name each one singular UPPER_SNAKE (`CUSTOMER`, `LINE_ITEM`), so relationship labels read as sentences (`CUSTOMER places ORDER`). When the user supplies a schema with plural table names (`line_items`), still use the singular entity and keep the real table name in the reply if it matters. Mermaid is case-sensitive about names.
2. For each foreign key, draw one relationship from the referenced (parent) table to the referencing (child) table.
3. Parent endpoint: it is `||` (exactly one) if the FK column is NOT NULL, `|o` (zero or one) if nullable.
4. Child endpoint: `o{` (zero or many) by default; `|{` (one or many) only if the schema or business rule forces at least one child; `o|` / `||` if the FK column is UNIQUE (or is the whole PK of the child).
5. Line, chosen per relationship: `--` identifying when that FK is part of the child's PK (weak entity, junction table with a composite key), `..` non-identifying otherwise, including a junction table with its own surrogate `id`.
6. Mark PK, FK, UK on columns. A composite PK is several `PK` rows.
7. Anything the schema does not settle (minimum child count, optional parent) is an assumption: choose the weaker option (`o{`, `|o`), and say so in the reply. Never copy cardinalities from an example.
8. When there is no junction table (the user or the schema only says that tags and articles, or students and courses, are many-to-many), draw one many-to-many line (`TAG }o..o{ ARTICLE`) and name it conceptual in the reply. When the schema does have the junction table, draw that table instead of the direct line (see "Traps").

## Cardinality symbols differ per endpoint

Read each side from the entity it touches. The left and right glyphs are mirror images:

| Meaning | Left endpoint | Right endpoint |
|---|---|---|
| Exactly one | `\|\|` | `\|\|` |
| Zero or one | `\|o` | `o\|` |
| One or many | `}\|` | `\|{` |
| Zero or many | `}o` | `o{` |

`}{` is not valid. Relationship form: `LEFT <left-glyph><line><right-glyph> RIGHT : "label"`; the label is mandatory (quote it if it has spaces).

```mermaid
erDiagram
    CUSTOMER ||..o{ ORDER : "places"
    ORDER ||--|{ LINE_ITEM : "contains"
    USER ||--o| PROFILE : "has"
    EMPLOYEE |o..o| BADGE : "holds"
    TAG }o..o{ ARTICLE : "labels"
    ORDER {
        int id PK
        int customer_id FK "NOT NULL"
        string number UK "human-facing"
    }
    LINE_ITEM {
        int order_id PK, FK "every order has at least one line"
        int line_no PK
    }
    PROFILE {
        int user_id PK, FK "shared key"
    }
    BADGE {
        int id PK
        int employee_id FK, UK "nullable"
    }
```

Each line follows the steps above: ORDER and BADGE have their own `id`, so their lines are `..`; LINE_ITEM and PROFILE carry the FK in their PK, so theirs are `--`. `|{` on LINE_ITEM comes from the stated business rule, `o|` on PROFILE because the schema does not force a profile, `|o` on EMPLOYEE because `employee_id` is nullable. TAG to ARTICLE is the conceptual many-to-many form.

## Traps

- Many-to-many: a conceptual ERD may draw it directly (`TAG }o..o{ ARTICLE`). When the schema has an actual junction table, draw that table as an entity with one relationship to each side, choosing each line and endpoint independently by the rules above.
- Attribute order is `type name [PK|FK|UK] ["comment"]`. A type with spaces breaks the parser. A type with parentheses such as `decimal(10,2)` parses in Mermaid 11.17 and 12.3 (tested 2026-11-13); if the target renderer rejects it, write `decimal` and move the precision into the comment.
- Entity names with spaces need quotes; attribute names cannot contain spaces.
- ERDs show structure, not behavior: soft-delete columns, audit trails and polymorphic references are plain columns here; do not invent relationships for them.

## Worked schemas

Two full schemas for requests that name a blog or a social network. They follow the steps above (parent to child, NOT NULL foreign key gives `||`, nullable gives `|o`, composite-key junction tables use `--`, own-id tables use `..`); never copy their cardinalities into a different schema. Both rendered with mmdc 12.2.0 (checked 2026-11-14).

### Blog platform: posts, comments, tags and a junction table

`POST_TAG` is the real junction table of the many-to-many between posts and tags, so the direct `POST }o--o{ TAG` line is not drawn as well. `LIKE.likeable_id` points at a post or a comment through `likeable_type`, so it is a plain column and has no relationship line.

```mermaid
erDiagram
    USER ||..o{ POST : "writes"
    USER ||..o{ COMMENT : "writes"
    POST ||..o{ COMMENT : "receives"
    COMMENT |o..o{ COMMENT : "is replied to by"
    CATEGORY |o..o{ POST : "groups"
    CATEGORY |o..o{ CATEGORY : "is parent of"
    POST ||--o{ POST_TAG : "is labelled by"
    TAG ||--o{ POST_TAG : "labels"
    USER ||..o{ LIKE : "gives"

    USER {
        bigint id PK "AUTO_INCREMENT"
        varchar email UK "NOT NULL"
        varchar username UK "NOT NULL"
        varchar password_hash "NOT NULL"
        varchar display_name
        text bio
        varchar avatar_url
        timestamp created_at "DEFAULT NOW()"
        timestamp last_login
    }

    POST {
        bigint id PK "AUTO_INCREMENT"
        bigint user_id FK "NOT NULL"
        bigint category_id FK "nullable"
        varchar title "NOT NULL"
        varchar slug UK "NOT NULL"
        text content "NOT NULL"
        text excerpt
        varchar featured_image_url
        varchar status "NOT NULL DEFAULT 'draft'"
        int view_count "DEFAULT 0"
        timestamp published_at
        timestamp created_at "DEFAULT NOW()"
        timestamp updated_at
    }

    COMMENT {
        bigint id PK "AUTO_INCREMENT"
        bigint user_id FK "NOT NULL"
        bigint post_id FK "NOT NULL"
        bigint parent_comment_id FK "nullable"
        text content "NOT NULL"
        varchar status "DEFAULT 'pending'"
        timestamp created_at "DEFAULT NOW()"
    }

    CATEGORY {
        bigint id PK "AUTO_INCREMENT"
        varchar name UK "NOT NULL"
        varchar slug UK "NOT NULL"
        text description
        bigint parent_id FK "nullable"
    }

    TAG {
        bigint id PK "AUTO_INCREMENT"
        varchar name UK "NOT NULL"
        varchar slug UK "NOT NULL"
    }

    POST_TAG {
        bigint post_id PK, FK "composite key"
        bigint tag_id PK, FK "composite key"
    }

    LIKE {
        bigint id PK "AUTO_INCREMENT"
        bigint user_id FK "NOT NULL"
        varchar likeable_type "NOT NULL"
        bigint likeable_id "polymorphic, no FK"
        timestamp created_at "DEFAULT NOW()"
    }
```

### Social network: follows, messages, notifications and groups

`FOLLOW` and `MESSAGE` each hold two foreign keys to `USER`, so each gets two relationship lines whose labels name the column. Group membership needs the `GROUP_MEMBER` junction table; the table is `CHAT_GROUP` because `GROUP` is an SQL reserved word. `NOTIFICATION.related_entity_id` is polymorphic, so it is a plain column. This schema renders about 2700 px wide, which a 900 px column shrinks until the text is hard to read: split it by area (posts, messaging, groups) for a README.

```mermaid
erDiagram
    USER ||..o{ POST : "creates"
    USER ||..o{ FOLLOW : "follows through follower_id"
    USER ||..o{ FOLLOW : "is followed through following_id"
    POST ||..o{ LIKE : "receives"
    POST ||..o{ COMMENT : "has"
    COMMENT |o..o{ COMMENT : "is replied to by"
    USER ||..o{ LIKE : "gives"
    USER ||..o{ COMMENT : "makes"
    USER ||..o{ NOTIFICATION : "receives"
    POST ||..o{ POST_MEDIA : "contains"
    USER ||..o{ MESSAGE : "sends through sender_id"
    USER ||..o{ MESSAGE : "receives through receiver_id"
    USER ||..o{ CHAT_GROUP : "creates through created_by"
    CHAT_GROUP ||--o{ GROUP_MEMBER : "has"
    USER ||--o{ GROUP_MEMBER : "joins as"

    USER {
        uuid id PK
        varchar username UK "NOT NULL"
        varchar email UK "NOT NULL"
        varchar password_hash "NOT NULL"
        varchar full_name
        text bio
        varchar profile_picture_url
        varchar cover_photo_url
        boolean is_verified "DEFAULT FALSE"
        boolean is_private "DEFAULT FALSE"
        timestamp created_at "DEFAULT NOW()"
    }

    POST {
        uuid id PK
        uuid user_id FK "NOT NULL"
        text content
        varchar visibility "DEFAULT 'public'"
        int likes_count "DEFAULT 0"
        int comments_count "DEFAULT 0"
        int shares_count "DEFAULT 0"
        timestamp created_at "DEFAULT NOW()"
        timestamp edited_at
    }

    POST_MEDIA {
        uuid id PK
        uuid post_id FK "NOT NULL"
        varchar media_type "NOT NULL"
        varchar media_url "NOT NULL"
        int display_order
    }

    FOLLOW {
        uuid id PK
        uuid follower_id FK "NOT NULL"
        uuid following_id FK "NOT NULL"
        timestamp created_at "DEFAULT NOW()"
    }

    LIKE {
        uuid id PK
        uuid user_id FK "NOT NULL"
        uuid post_id FK "NOT NULL"
        timestamp created_at "DEFAULT NOW()"
    }

    COMMENT {
        uuid id PK
        uuid user_id FK "NOT NULL"
        uuid post_id FK "NOT NULL"
        uuid parent_comment_id FK "nullable"
        text content "NOT NULL"
        int likes_count "DEFAULT 0"
        timestamp created_at "DEFAULT NOW()"
    }

    MESSAGE {
        uuid id PK
        uuid sender_id FK "NOT NULL"
        uuid receiver_id FK "NOT NULL"
        text content "NOT NULL"
        boolean is_read "DEFAULT FALSE"
        timestamp created_at "DEFAULT NOW()"
        timestamp read_at
    }

    NOTIFICATION {
        uuid id PK
        uuid user_id FK "NOT NULL"
        varchar notification_type "NOT NULL"
        text content "NOT NULL"
        boolean is_read "DEFAULT FALSE"
        varchar related_entity_type
        uuid related_entity_id "polymorphic, no FK"
        timestamp created_at "DEFAULT NOW()"
    }

    CHAT_GROUP {
        uuid id PK
        varchar name "NOT NULL"
        text description
        uuid created_by FK "NOT NULL"
        boolean is_private "DEFAULT FALSE"
        timestamp created_at "DEFAULT NOW()"
    }

    GROUP_MEMBER {
        uuid group_id PK, FK "composite key"
        uuid user_id PK, FK "composite key"
    }
```
