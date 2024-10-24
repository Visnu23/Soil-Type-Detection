// Initialize Firebase (Assuming you've added the Firebase script in the HTML)
// const firebaseConfig = { ... };
const firebaseConfig = {
    apiKey: "AIzaSyAVj3UlbvOTAqtuRAZoAoaoDDq30nSRG50",
    authDomain: "index-page-50687.firebaseapp.com",
    databaseURL: "https://index-page-50687-default-rtdb.firebaseio.com",
    projectId: "index-page-50687",
    storageBucket: "index-page-50687.appspot.com",
    messagingSenderId: "352434399664",
    appId: "1:352434399664:web:cb53a413fafeba94378e75"
  };
  
  // initialize firebase
  firebase.initializeApp(firebaseConfig);
  

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Firebase code to store user registration
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            // Signed in 
            alert('Registration successful');
            // Store additional user info if necessary
        })
        .catch((error) => {
            alert('Registration failed: ' + error.message);
        });
});
