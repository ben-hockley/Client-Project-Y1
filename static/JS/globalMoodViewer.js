document.addEventListener("DOMContentLoaded", function () {
    fetch('/GlobalMoodData')
    .then(response => response.json())
    .then(data => {
        const grid = document.getElementById('userGrid');
        let emojiList = ["&#128545","&#128544","&#128546","&#128577","&#128528","&#128578","&#128512","&#129321","&#129322"];
        const columns = 4;

        for (let i = 0; i < data.length; i += columns) {
            const rowChunk = data.slice(i, i + columns);

            const row = document.createElement('div');
            row.classList.add('row');

            rowChunk.forEach(tuple => {
                const userBox = document.createElement('div');
                userBox.classList.add('user');

                const firstName = tuple[0];
                const surName = tuple[1];
                const mood = tuple[2];

                userBox.innerHTML = `
                    <p>${emojiList[mood]} ${firstName} ${surName}</p>
                `;
                row.appendChild(userBox);
            });

            grid.appendChild(row);
        }
    })
    .catch(error => console.error('Error fetching data:', error));
});