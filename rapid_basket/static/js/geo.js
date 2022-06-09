const getLocation = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition)
    }
}

const showPosition = async (position) => {
    const lat = await position.coords.latitude
    const lon = await position.coords.longitude
    const agent = navigator.userAgent
    const url = '/get_user_into/'

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ lat, lon, agent })
    }).then((res) => res.json());
}
