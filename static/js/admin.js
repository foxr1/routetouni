/*!
 * Name: Katie Fallon
 * All functions required for the admin.html page.
 */


/**
 * If the user is verified as a peer mentor, verified attribute is updated
 * to be true in Firebase Database
 *
 * @param {string} uid      The uid of the user verified
 */
function isPeerMentor(uid) {
    firebase.database().ref('users/' + uid).update({
        mentor_verified: true
    }) .then(() => {
        location.reload();
    });
}

/**
 * If the user is rejected as being a peer mentor,
 * their role is changed to student in the firebase database
 *
 * @param {string} uid      The uid of the user rejected
 */
function notPeerMentor(uid) {
    firebase.database().ref('users/' + uid).update({
        role: 'Student'
    }) .then(() => {
        location.reload();
    });
}

/**
 * Function allowing Admin to filter View All Peer Mentors table by school
 * from https://www.w3schools.com/howto/howto_js_filter_table.asp
 */
function searchByCourse() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("school_input");
    filter = input.value.toUpperCase();
    table = document.getElementById("displaypm_table");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}