/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2500,
    delay: 400,
    // reset: true
})

sr.reveal(`.about__Unveil`)
sr.reveal(`.about,.about`, {delay: 500})
sr.reveal(`.home__social`, {delay: 600})
sr.reveal(`.about_section, .layout_padding`,{origin: 'left'})
sr.reveal(`.about__data, .contact__form,.main-widget`,{origin: 'right'})
sr.reveal(`.steps__card, .product__card, .questions__group, .footer`,{interval: 100})