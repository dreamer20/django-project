function getLocalDateTimeString(dateTimeString) {
    function appendZero(value) {
        return value < 10 ? '0' + value : value
    }
    d = new Date(dateTimeString);
    const hours = appendZero(d.getHours())
    const minutes = appendZero(d.getMinutes())
    const month = appendZero(d.getMonth() + 1)
    const day = appendZero(d.getDate())
    const year = d.getFullYear().toString().slice(-2)
    const time = `${hours}:${minutes}`
    const date = `${day}.${month}.${year}`

    return {
        date,
        time
    }

}

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

const dateElems = document.querySelectorAll('.publication-date')
dateElems.forEach(el => {
    const dateTime = getLocalDateTimeString(el.textContent)
    el.textContent = `${dateTime.date} at ${dateTime.time}`
});

