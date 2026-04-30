## Table `branch_subjects`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `branch_id` | `uuid` |  Nullable |
| `subject_id` | `uuid` |  Nullable |
| `year_id` | `uuid` |  Nullable |
| `semester` | `int4` |  |

## Table `branches`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  Unique |

## Table `images`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `question_id` | `uuid` |  Nullable |
| `image_url` | `text` |  |
| `order_index` | `int4` |  Nullable |

## Table `pyq_sources`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `year` | `int4` |  |
| `exam_type` | `exam_type_enum` |  |
| `season` | `season_enum` |  |
| `question_number` | `text` |  |
| `subject_id` | `uuid` |  Nullable |

## Table `question_pyq_map`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `question_id` | `uuid` |  Nullable |
| `pyq_source_id` | `uuid` |  Nullable |

## Table `question_topics`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `question_id` | `uuid` |  Nullable |
| `topic_id` | `uuid` |  Nullable |

## Table `questions`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `question_text` | `text` |  |
| `difficulty` | `difficulty_enum` |  |

## Table `subjects`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  |
| `code` | `text` |  Unique |
| `pyq_drive_link` | `text` |  Nullable |
| `notes_drive_link` | `text` |  Nullable |
| `course_outcome_link` | `text` |  Nullable |

## Table `topic_resources`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `topic_id` | `uuid` |  Nullable |
| `resource_type` | `text` |  Nullable |
| `title` | `text` |  Nullable |
| `url` | `text` |  Nullable |

## Table `topics`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `subject_id` | `uuid` |  Nullable |
| `name` | `text` |  |
| `summary` | `text` |  Nullable |

## Table `years`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  Unique |

