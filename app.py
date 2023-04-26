from flask import Flask, render_template, request
from pybtex.database import parse_string, Entry, BibliographyData
import Levenshtein
from venue import venues_list
import os
app = Flask(__name__)

def findVenues(booktitle):
    highest_sim = 0
    highest_sim_key = ''
    for key, val in venues_list.items():
        # Sometimes Google Scholar gives the short venue name
        if booktitle == key:
            return key
        # compare the booktitle with full venue name
        sim = 1 - Levenshtein.distance(booktitle, val[0]) / max(len(booktitle), len(val[0]))
        if sim > highest_sim:
            highest_sim = sim
            highest_sim_key = key

    if highest_sim > 0.7:
        return highest_sim_key
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        text = request.form['bibliography']
        short = request.form.get('s_venue') # use short venue name or not
        bib_data = parse_string(text, 'bibtex')

        bib_data_new = BibliographyData(entries={}) # new bib data with updated venue names
        bib_data_bad = BibliographyData(entries={}) # entries that can not find the venue

        for key, entry in bib_data.entries.items():
            # we assume that the entry has title and year
            if 'title' not in entry.fields or 'year' not in entry.fields:
                continue
            
            if 'booktitle' in entry.fields:
                booktitle = entry.fields['booktitle']
            elif 'journal' in entry.fields:
                booktitle = entry.fields['journal']
            elif 'archivePrefix' in entry.fields:
                booktitle = entry.fields['archivePrefix']
            else:
                booktitle = ''

            venue_key = findVenues(booktitle)
            if venue_key is not None:
                new_entry = Entry(entry.type, fields={'title': entry.fields['title'], 'year': entry.fields['year'],
                                                      'booktitle': venues_list[venue_key][0] if short is None else venues_list[venue_key][1]}, persons=entry.persons)
                new_key = entry.persons['author'][0].last_names[0].lower() + entry.fields['year'] + venue_key.lower()
                bib_data_new.add_entry(new_key, new_entry)
            else:
                new_entry = Entry(entry.type, fields={'title': entry.fields['title'], 'year': entry.fields['year'], 'booktitle': booktitle}, persons=entry.persons)
                new_key = key
                bib_data_bad.add_entry(new_key, new_entry)

        if len(bib_data_bad.entries) == 0:
            output = bib_data_new.to_string('bibtex')
        else:
            output = bib_data_new.to_string('bibtex') + '\n\n\n\n###### Can not find the venue for the following entries #####\n' + bib_data_bad.to_string('bibtex')

        return render_template('index.html', bibliography=output)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT', 40000))