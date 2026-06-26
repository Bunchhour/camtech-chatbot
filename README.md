# CamTech Chatbot

## Data Directory Structure

```
data/
  about_camtech.md
  faculties.md
  research_and_innovation.md
  admissions/
    Academic_Info_ENG_2023_2024.md
    ai_university.md
    application_process.md
  bachelor_degree/
    built_enviroment/
      architectures.md
      interior_design.md
    business/
      business_and_risk.md
    engineering/
      cybersecurity.md
      data_science_and_ai.md
      robotic_and_automation.md
      software_engineer.md
  masters_and_PhD/
    school_of_graduate_studies.md
  school_of_contuing_edu/
    business_data_driven.md
    digital_skill_business_success.md
    profess_cert_teaching_methods.md
```

**============== Chunking Process Splitting Document  ==========================**
This code is doing **Markdown-aware chunking**. Instead of splitting text randomly every 500 characters, it splits according to your Markdown headings (`#`, `##`, `###`).

Let's go through it line by line.

---

## Step 1: Create the Markdown splitter

```python
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "H1"),
        ("##", "H2"),
        ("###", "H3")
    ]
)
```

This tells LangChain:

| Markdown | Metadata Name |
| -------- | ------------- |
| `#`      | H1            |
| `##`     | H2            |
| `###`    | H3            |

Example Markdown:

```markdown
# Admissions

General admission information.

## Required Documents

Bring transcript and diploma.

## Application Process

Submit online application.

### Step 1

Create account.

### Step 2

Upload documents.
```

The splitter understands the document hierarchy.

---

## Step 2: Create an empty list

```python
md_docs = []
```

This list will store all the chunks after splitting.

Initially:

```python
md_docs = []
```

---

## Step 3: Loop through all loaded documents

```python
for doc in documents:
```

Suppose:

```python
documents
```

contains:

```python
[
    Document(source="admissions.md"),
    Document(source="faculties.md"),
    Document(source="about_camtech.md")
]
```

The loop processes them one by one.

---

## Step 4: Split the document

```python
splits = markdown_splitter.split_text(doc.page_content)
```

Suppose `doc.page_content` is:

```markdown
# Admissions

General information.

## Required Documents

Transcript
Diploma

## Application Process

Apply online.
```

After splitting:

```python
splits
```

becomes approximately:

```python
[
    Document(
        page_content="General information.",
        metadata={"H1": "Admissions"}
    ),

    Document(
        page_content="Transcript\nDiploma",
        metadata={
            "H1": "Admissions",
            "H2": "Required Documents"
        }
    ),

    Document(
        page_content="Apply online.",
        metadata={
            "H1": "Admissions",
            "H2": "Application Process"
        }
    )
]
```

Notice:

* Text is separated by section
* Heading information is stored in metadata

This is extremely useful for RAG.

---

## Step 5: Preserve the original file source

```python
for split in splits:
    split.metadata['source'] = doc.metadata.get(
        'source',
        'unknown'
    )
```

Before this:

```python
{
    "H1": "Admissions",
    "H2": "Required Documents"
}
```

After this:

```python
{
    "H1": "Admissions",
    "H2": "Required Documents",
    "source": "../data/admissions/application_process.md"
}
```

Now each chunk remembers which file it came from.

Without this, you might lose source tracking.

---

## Step 6: Add chunks to the final list

```python
md_docs.extend(splits)
```

Suppose:

```python
splits = [
    chunk1,
    chunk2,
    chunk3
]
```

Then:

```python
md_docs.extend(splits)
```

is similar to:

```python
md_docs.append(chunk1)
md_docs.append(chunk2)
md_docs.append(chunk3)
```

After processing all files:

```python
md_docs
```

contains every chunk from every Markdown file.

---

# Visual Example

Suppose you have:

```markdown
# Bachelor of Data Science and AI

The program lasts 4 years.

## Career Opportunities

Graduates can become:
- Data Scientists
- AI Engineers

## Curriculum

Students learn:
- Python
- Machine Learning
```

After splitting:

### Chunk 1

```python
{
    "page_content":
        "The program lasts 4 years.",

    "metadata": {
        "H1": "Bachelor of Data Science and AI"
    }
}
```

### Chunk 2

```python
{
    "page_content":
        "Graduates can become Data Scientists and AI Engineers.",

    "metadata": {
        "H1": "Bachelor of Data Science and AI",
        "H2": "Career Opportunities"
    }
}
```

### Chunk 3

```python
{
    "page_content":
        "Students learn Python and Machine Learning.",

    "metadata": {
        "H1": "Bachelor of Data Science and AI",
        "H2": "Curriculum"
    }
}
```

---

# Why this is good for your CamTech chatbot

If a user asks:

> What careers can Data Science students pursue?

The vector search can retrieve:

```text
Graduates can become:
- Data Scientists
- AI Engineers
```

And the metadata tells the LLM:

```python
{
    "H1": "Bachelor of Data Science and AI",
    "H2": "Career Opportunities"
}
```

So the model knows the context is specifically:

> Career Opportunities under the Bachelor of Data Science and AI program.

This usually performs much better than embedding an entire 5-page document as one chunk.

**========================= End =====================================**
