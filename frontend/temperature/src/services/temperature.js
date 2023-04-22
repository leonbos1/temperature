import data from '../data.json';

const url = data["url"];

export const getCurrentTemperature = () => {
    return fetch(url)
        .then(response => response.json())
        .then(data => data.temperature);
}

export const getDailyTemperature = () => {
    return fetch(url)
        .then(response => response.json())
        .then(data => data.daily);
}

export const getWeeklyTemperature = () => {
    return fetch(url)
        .then(response => response.json())
        .then(data => data.weekly);
}

export const getMonthlyTemperature = () => {
    return fetch(url)
        .then(response => response.json())
        .then(data => data.monthly);
}

