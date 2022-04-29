async function getArtist(artist_id) {
    let url = `http://127.0.0.1:8000/artist/${artist_id}`
    let artist = fetch(url)
    .then(response => response.json())
    .then(data => {console.log(data)})
    .catch(error => console.log(error));

    return artist;
}

async function getArtists() {
    let artists = fetch('http://127.0.0.1:8000/artists')
    .then(response => response.json())
    .then(data => {console.log(data)})
    .catch(error => console.log(error));

    return [artists];
}

async function buildArtistTable() {
    let artists = fetch('http://127.0.0.1:8000/artists')
    .then(response => response.json())
    .then((data) => {
        let heading = document.createElement('h2');
        heading.textContent = 'Your Artists';

        let table = document.createElement('table');
        table.setAttribute('id', 'artistsTable');

        let header = document.createElement('tr');
        header.innerHTML = '<th>Artist</th><th>Total Playtime</th><th>User Score</th></tr>';
        table.append(header);

        var result = [];

        for (var i in data) result.push([data [i]]);
        

        result = result[2][0];

        result.forEach(artist => {
            let name = document.createElement('td');
            name.textContent = artist.name;

            let totalPlaytime = document.createElement('td');
            totalPlaytime.textContent = artist.total_playtime;

            let userScore = document.createElement('td');
            userScore.textContent = artist.user_score;

            let row = document.createElement('tr');
            row.append(name, totalPlaytime, userScore);
            table.appendChild(row);
        });

        let artists = new DocumentFragment();
        artists.append(heading, table);

        let body = document.getElementById("dataPane");
        body.append(artists); 

    })
    .catch(error => console.log(error));
}

export { buildArtistTable };

