$('.nav-pills a').on('show.bs.tab', function () {
    setTimeout(function () {
        $('img').maphilight({
            fillColor: '00ff00',
            fillOpacity: 0.5,
        })
    }, 500);
});
