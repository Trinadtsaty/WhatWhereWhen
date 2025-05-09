const stars = document.querySelectorAll('.star');

const stars_full = document.querySelectorAll('.full');
let che = false
console.log(question_number)

if (!estimation_ball_bol) {
    stars_full.forEach(star_full => {
        star_full.style.display = 'none';
    });
} else {
    stars_ligt(my_estimation)
    che = true
};

const URL_server = 'http://127.0.0.1:8000'
const URL_adress = '/questions/api/v1'

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли cookie с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function POST(data, URL) {
    fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Указываем тип контента
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
    })

};
function PUT(data, URL) {
    fetch(URL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json', // Указываем тип контента
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
    })
};




function stars_ligt(number) {
    stars_unligt(10)
    for (var i=1; i<=number; i++) {
        const element_full = document.querySelector(`#star_${i}_full`);
        const element_unfull = document.querySelector(`#star_${i}_unfull`);
        element_full.style.display = 'block';
        element_unfull.style.display = 'none';

    };
};

function stars_unligt(number) {
    for (var i=1; i<=number; i++) {
        const element_full = document.querySelector(`#star_${i}_full`);
        const element_unfull = document.querySelector(`#star_${i}_unfull`);
        element_full.style.display = 'none';
        element_unfull.style.display = 'block';
    };
};


stars.forEach(star => {
    star.addEventListener('mouseover', function() {
        const number = star.getAttribute('data-value');
        if (!che) {
            stars_ligt(number)
        };
    });
    star.addEventListener('click', function() {
        const number = star.getAttribute('data-value');
        stars_ligt(number)
        const data = {
            "question": question_number,
            "estimation": number
        }
        if (che) {
            PUT(data, URL_server + URL_adress)
        } else {
            POST(data, URL_server + URL_adress)
        };
        che = true;

    });
    star.addEventListener('mouseout', function() {
        const number = star.getAttribute('data-value');
        if (!che) {
            stars_unligt(number)
        };
    });
});





