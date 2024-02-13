import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from ajouter_ticket import ajouter_ticket


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
today = datetime.now()


@app.route('/')
def index():
    return render_template(
        'index.html', clubs=clubs, competitions=competitions
    )


@app.route('/showSummary', methods=['POST'])
def showSummary():
    comp = [
        competition for competition in competitions
        if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today
    ]
    matching_clubs = [
        club for club in clubs
        if club['email'] == request.form['email']
    ]
    if not matching_clubs:
        flash("L'e-mail fourni n'existe pas dans notre système.", 'error')
        # Redirigez vers la page où l'erreur doit être affichée
        return redirect(url_for('index'))
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=comp)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html', club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html', club=club, competitions=competitions
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [
        c for c in competitions
        if c['name'] == request.form['competition']
    ][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired <= 0:
        flash("le nombre fourni n'est pas valide.", 'error')
        # Redirigez vers la page où l'erreur doit être affichée
        return redirect(url_for(
            'book', club=club['name'], competition=competition['name']
            ))
    if placesRequired <= int(club['points']) and placesRequired <= 12:
        # Tente d'ajouter les tickets
        if ajouter_ticket(club['name'], competition['name'], placesRequired):
            # Si l'ajout est réussi,mettez à jour les informations et redirigez
            competition['numberOfPlaces'] = (
                int(competition['numberOfPlaces']) - placesRequired
            )
            club['points'] = int(club['points']) - placesRequired
            flash('Great-booking complete!', "success")
            return redirect(url_for(
                'book', club=club['name'], competition=competition['name']
                ))
        else:
            # Si l'ajout a échoué, affichez un message approprié
            flash("Impossible d'ajouter tickets, limite dépassée.", "error")
            return redirect(url_for(
                'book', club=club['name'], competition=competition['name']
                ))

    if placesRequired >= int(competition['numberOfPlaces']):
        flash("le nombre fourni est superieur au nombre de place.", 'error')
        # Redirigez vers la page où l'erreur doit être affichée
        return redirect(url_for(
            'book', club=club['name'], competition=competition['name']
            ))
    if placesRequired > int(club['points']):
        flash(
            "le nombre fourni superieur au points du club.", 'error'
        )
        # Redirigez vers la page où l'erreur doit être affichée
        return redirect(url_for(
            'book', club=club['name'], competition=competition['name']
            ))

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/some_other_route/<club_email>')
def some_other_route(club_email):
    comp = [
        competition for competition in competitions
        if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today
    ]
    matching_clubs = [club for club in clubs if club['email'] == club_email]
    if not matching_clubs:
        flash("L'e-mail fourni n'existe pas dans notre système.", 'error')
        # Redirigez vers la page où l'erreur doit être affichée
        return redirect(url_for('index'))
    club = matching_clubs[0]
    # Vous pouvez effectuer des opérations supplémentaires ici si nécessaire
    return render_template('welcome.html', club=club, competitions=comp)
