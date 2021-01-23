// Configuration for Firebase
var firebaseConfig = {
    apiKey: "AIzaSyCl6CgDwOVVxdvQou38U-v71tZHoH9Fx-k",
    authDomain: "route2uni.firebaseapp.com",
    projectId: "route2uni",
    storageBucket: "route2uni.appspot.com",
    messagingSenderId: "1081173404847",
    appId: "1:1081173404847:web:ac22f051b174e6b142785a",
    measurementId: "G-DE01D2GM7L",
    databaseUrl: "https://route2uni-default-rtdb.firebaseio.com/"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();
var database = firebase.database();
var storage = firebase.storage();