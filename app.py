from flask import Flask, render_template, request
from pybtex.database import parse_string, Entry, BibliographyData

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        text = request.form['bibliography']

        bib_data = parse_string(text, 'bibtex')

        bib_data_new = BibliographyData(entries={})

        for key, entry in bib_data.entries.items():
            if 'title' not in entry.fields \
                or 'year' not in entry.fields:
                continue
            
            if 'booktitle' in entry.fields:
                booktitle = entry.fields['booktitle']
            elif 'journal' in entry.fields:
                booktitle = entry.fields['journal']
            elif 'archivePrefix' in entry.fields:
                booktitle = entry.fields['archivePrefix']

            new_entry = Entry(entry.type, fields={'title': entry.fields['title'], 'year': entry.fields['year'], 'booktitle': booktitle}, persons=entry.persons)
            new_key = entry.persons['author'][0].last_names[0].lower() + entry.fields['year']
            bib_data_new.add_entry(new_key, new_entry)

    return render_template('index.html', bibliography=bib_data_new.to_string('bibtex'))

if __name__ == '__main__':
    app.run(port=8000)