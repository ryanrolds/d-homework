
let updateTimer = null
const updateInterval = 60000 // 1 minute
document.addEventListener("DOMContentLoaded", function() {
    updateTimer = setInterval(() => {
        try {
            updateSensors()
        } catch (e) {
            console.error(e)
        }
    }, updateInterval)
});

function updateSensors() {
    fetch('/sensors')
        .then((response) => {
            if (response.status !== 200) {
                throw new Error("Something went wrong")
            }

            return response.json()
        })
        .then((data) => {
            if (!data || data.status !== "ok") {
                throw new Error("Something is wrong with the response data")
            }

            data.sensors.forEach((sensor) => {
                const sensorElm = document.getElementById(`sensor-${sensor.mac_address}`)
                if (!sensorElm) {
                    // Could be a sensor that first checked in after the page loaded
                    // TODO handle adding new sensors after page load
                    return
                }

                const lastHeartbeatElm = sensorElm.querySelector(".last-heartbeat")
                lastHeartbeatElm.innerHTML = sensor.last_heartbeat
            })
        })
}
