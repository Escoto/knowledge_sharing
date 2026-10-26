# Writing rules (based on ASD-STE100)

ASD-STE100 Simplified Technical English (STE) is a controlled language. Aerospace teams made it for
maintenance manuals that people read in their second language. The same rules make engineering
guides easy for junior engineers and non-native readers.

This file is a short working summary written for this skill. It is not the official spec. The
official spec, with the full dictionary of approved words, is available from ASD
(https://www.asd-ste100.org). Use that dictionary when a team needs strict compliance.

## Contents
1. Words
2. Sentences
3. Procedures (instructions)
4. Descriptive text
5. Warnings and notes
6. Common word swaps
7. Self-check before you show the page

---

## 1. Words

- **One word, one meaning.** Use a word with one meaning only. "Run" is the action of starting a job.
  Do not also use "run" for "a set of rows".
- **One meaning, one word.** Pick one term for each thing and keep it on the whole page. If the page
  says "field", do not change to "attribute", "property" or "key" later. Put the terms in a small
  "Term / Meaning on this page" table in the Purpose section.
- **Technical names are allowed.** Names of settings, tables, files, functions, error messages and
  products stay as they are, in `code` format. Do not simplify a name that the reader must type.
- **Use simple verbs in their simple forms.** Prefer present tense, simple past, and future with "will".
  Avoid "-ing" forms as nouns or adjectives ("the processing of" → "when the job processes").
- **Do not make verbs into nouns.** "Do a check of the table" is acceptable STE. "Perform validation
  of" is not. Prefer the verb: "Check the table."
- **Use articles** ("the", "a", "an") where normal English has them. They make the sentence clear.
- **No slang, idioms, or jokes.** "Under the hood", "out of the box", "a no-op" are hard for
  non-native readers.

## 2. Sentences

- **Short sentences.** Maximum 20 words in a procedure step. Maximum 25 words in descriptive text.
  Most sentences can be much shorter.
- **One topic per sentence.** If a sentence has "and" between two different ideas, make two sentences.
- **Active voice.** "The pusher removes the field." not "The field is removed by the pusher." Passive
  voice is acceptable only when the actor is not known or not important, and then rarely.
- **Keep paragraphs short.** Maximum 6 sentences. Each paragraph has one topic.
- **Put the condition first.** "If the field is missing, the push stops." The reader knows the
  context before the result.

## 3. Procedures (instructions)

- **Imperative form.** "Open the file." not "You should open the file." or "The file must be opened."
- **One instruction per sentence.** Two actions that occur at the same time can be in one sentence.
- **One step per numbered item.** A step can have one or two short sentences: the action and, if
  necessary, what the reader must see after it.
- **Give the location before the action** when the reader must find something: "In the `push_config`
  section, add `exclude_from_payload`."
- **Write negative instructions clearly**: "Do not change `drop_columns`."
- **Tell the reader the result** they must get, so that they know the step is correct.

## 4. Descriptive text

- Start with the most important information.
- Tell the reader what a thing does, then why. "The job reads the rows first, because all the next
  steps use these rows."
- Use "because", "so", "if", "when", "before", "after" to show the logic. Do not leave the reader to
  guess why the order is important.
- Use "Thus," or "Then," at the start of a sentence to connect two short sentences, not a long
  sentence with many clauses.

## 5. Warnings and notes

- A **warning** (yellow `warn` panel) tells the reader about a mistake that breaks something. Start
  with a short command in bold: "**Do not add `record_id` to `drop_columns`.**" Then tell the result
  of the mistake in one or two sentences.
- A **note** (purple `note` panel) gives information that is necessary but is not an instruction,
  for example a version requirement.
- A **summary** (green `ok` panel) closes a concept section with the one rule the reader must keep.
- Do not put instructions in a note. Put them in the procedure.
- For all five panel types, good and bad examples, and where caveats go, read
  `callouts-and-caveats.md`.

## 6. Common word swaps

These are frequent swaps. They come from general STE practice; check the official dictionary for
strict work.

| Avoid | Use |
|---|---|
| ensure | make sure |
| utilize, leverage | use |
| perform, execute (an action) | do, run |
| obtain, retrieve | get |
| commence, initiate | start |
| terminate, abort | stop |
| prior to | before |
| subsequent, following | next, after |
| in order to | to |
| due to | because of |
| approximately | about |
| via | through, with |
| allow, enable (someone to) | let, make it possible to |
| should (in an instruction) | imperative ("Do X.") or "must" |
| e.g. / i.e. / etc. | for example / that is / (list the items) |
| simply, just, easily, obviously | (delete the word) |
| in case of | if |
| might, may, probably (about what the software does) | "can", or state the condition: "If X, then Y." |
| is able to | can |
| a number of | some, many, or the number |

## 7. Self-check before you show the page

1. Run `scripts/ste_check.py <page.html>` and fix every long sentence and every flagged word, or keep
   it on purpose (for example, a name the reader must type).
2. Read each procedure step aloud. If it has two actions, split it.
3. Look for a term that has two names on the page. Pick one.
4. Make sure that each "why" is stated, especially in the flow diagram notes.
