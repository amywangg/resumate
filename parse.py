import spacy, pytextrank, re

def text_rank(job):
    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    doc = nlp(job)

    # examine the top-ranked phrases in the document
    keywords = list(map(str, doc._.phrases))

    buzzwords = [line.rstrip('\n').lower() for line in open("static/BuzzWords.txt")]
    buzzwords = [x.strip(' ') for x in buzzwords]

    matches = []

    for word in buzzwords:
        if any(word in s for s in keywords):
            matches.append(word)

    return matches

def match_skills(app_skills, job_skills):
    matches = []
    for word in job_skills:
        if any(word.lower() in s.lower() for s in app_skills):
            matches.append(word)
    return matches