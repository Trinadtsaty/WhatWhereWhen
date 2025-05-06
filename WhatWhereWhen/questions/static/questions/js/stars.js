const stars = document.querySelectorAll('.star');

const stars_full = document.querySelectorAll('.full');
let che = false

if (!estimation_ball_bol) {
    stars_full.forEach(star_full => {
        star_full.style.display = 'none';
    });

} else {
    stars_ligt(my_estimation)
    let che = true
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
        che = true;
        stars_ligt(number)
    });
    star.addEventListener('mouseout', function() {
        const number = star.getAttribute('data-value');
        if (!che) {
            stars_unligt(number)
        };
    });
});




