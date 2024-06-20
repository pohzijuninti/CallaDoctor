const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const app = express();
const bcrypt = require('bcryptjs')
app.use(express.json());

// add body-parser middleware to parse request bodies
app.use(bodyParser.urlencoded({ extended: false }));

const hospital = [
  {
    "hospitalID": 1,
    "name": "Pantai Hospital Penang",
    "image": "pantai.png",
    "email": "pantai@gmail.com",
    "password": "$2a$10$grRJEbGhuED/Rz.9T0.SCOdPxESFm4CTBKs1d67s3W3wk8.uSDGsq"
  },
  {
    "hospitalID": 2,
    "name": "Island Hospital Penang",
    "image": "island.jpeg",
    "email": "island@gmail.com",
    "password": "$2a$10$ZVb20qG6EasQgkDZNT31yuIRAaR7MMcstvoYQyZK7v03PU1q9XyMO"
  },
  {
    "hospitalID": 3,
    "name": "Gleneagles Hospital Penang",
    "image": "gmc.jpeg",
    "email": "gmc@gmail.com",
    "password": "$2a$10$pbpLhUoBd0A/QQ2KvHYG9e7NVnlD6IVjDpyggctfeU23sxlxdlvrK"
  },
  {
    "hospitalID": 4,
    "name": "Sunway Medical Centre Penang",
    "image": "sunway.jpeg",
    "email": "sunway@gmail.com",
    "password": "$2a$10$IgdR5tTZmmzH00kYZ8BgVe88CXfpWcXIDg5CTuE/l7cGYBfpcYS92"
  },
  {
    "hospitalID": 5,
    "name": "Penang Adventist Hospital",
    "image": "adventist.jpeg",
    "email": "adventist@gmail.com",
    "password": "$2a$10$VQgehZMx9m9Q2X3OaNUCneupSP6SVhSkSKRFRX3l0OBlhcDvYket."
  },
];

const speciality = [
  {
    "specialityID": 11,
    "name": "Cardiology",
  },
  {
    "specialityID": 12,
    "name": "General Surgery",
  },
  {
    "specialityID": 13,
    "name": "Ophthalmology",
  },
  {
    "specialityID": 14,
    "name": "Dermatology",
  },
  {
    "specialityID": 15,
    "name": "Dentistry",
  },
];

let doctors = [
  {
    "doctorID": 21,
    "name": "Dr. Lim Guan Choon",
    "image": "gclim.png",
    "specialityID": 11,
    "hospitalID": 1,
    "email": "gclim@gmail.com",
    "password": "$2a$10$RefkciYGazZHYv.59jza5.y4GGvIc2DsMN5g6Fbw62PpQLMwJZP3O"
  },
  {
    "doctorID": 22,
    "name": "Dr. Wong Choy Hoong",
    "image": "chwong.jpeg",
    "specialityID": 13,
    "hospitalID": 1,
    "email": "chwong@gmail.com",
    "password": "$2a$10$BgXqQQcbstysnmYzhuZ59uoSWEFK9PcujdtqS/hQffndzZQvj7bZm"
  },
  {
    "doctorID": 23,
    "name": "Dr. Lai Huey Yoke",
    "image": "hylai.jpeg",
    "specialityID": 15,
    "hospitalID": 1,
    "email": "hylai@gmail.com",
    "password": "$2a$10$XAiqRRipwJN9cXqnYRzEKewXU2FkLfWeajbfRYJzh/4OiE0kCZt7u"
  },
  {
    "doctorID": 24,
    "name": "Dr. Goh Tiong Meng",
    "image": "tmgoh.png",
    "specialityID": 12,
    "hospitalID": 2,
    "email": "tmgoh@gmail.com",
    "password": "$2a$10$tz47aED4GEK0keHWXChK1.pvmbVNvCVdiQyy0SU2utEOaOPBnTMny"
  },
  {
    "doctorID": 25,
    "name": "Dr. Andrew Lim Keat Eu",
    "image": "andrew.png",
    "specialityID": 13,
    "hospitalID": 2,
    "email": "andrew@gmail.com",
    "password": "$2a$10$/dqF9WfM2olg..2K8f7AVeqW5B9B2lIwD3QnbpSvbD86gRyeahokK"
  },
{
    "doctorID": 26,
    "name": "Dr. Khor Yek Huan",
    "image": "yhkhor.png",
    "specialityID": 14,
    "hospitalID": 2,
    "email": "yhkhor@gmail.com",
    "password": "$2a$10$NVzoRyx1Z4E.1f1mpbw15OLpDqYf3u/na2QIAKALluNzFf.dLuOji"
  },
  {
    "doctorID": 27,
    "name": "Dr. Jasjit Singh",
    "image": "jasjit.jpeg",
    "specialityID": 12,
    "hospitalID": 3,
    "email": "jasjit@gmail.com",
    "password": "$2a$10$1dTAdoxwQDzSr.arTM1dMeh5OQ8NQ4dOwEvMvSucIm//s3dx4I8zq"
  },
  {
    "doctorID": 28,
    "name": "Dr. Amelia Lim Lay Suan",
    "image": "amelia.jpeg",
    "specialityID": 13,
    "hospitalID": 3,
    "email": "amelia@gmail.com",
    "password": "$2a$10$cKkzlRk.9CkaQ61eTiVItOxYylHZjrDFLWjSt7iz5J4QweIZOdEYa"
  },
  {
    "doctorID": 29,
    "name": "Dr. Chong Yew Thong",
    "image": "ytchong.jpeg",
    "specialityID": 14,
    "hospitalID": 3,
    "email": "ytchong@gmail.com",
    "password": "$2a$10$AiIJMQYi341v62mKJy0.pO09uxL8jJqXxPAGyRC0D5xT3R9JoCZ6y"
  },
  {
    "doctorID": 30,
    "name": "Dr. Khaw Chee Sin",
    "image": "cskhaw.png",
    "specialityID": 11,
    "hospitalID": 4,
    "email": "cskhaw@gmail.com",
    "password": "$2a$10$Z3KqOm4ZvYT25wqDstSGKOAhsrxhccmiAXZPj.p4cWo2lmcsPCVem"
  },
  {
    "doctorID": 31,
    "name": "Dr. Lee Kuo Ting",
    "image": "ktlee.png",
    "specialityID": 11,
    "hospitalID": 4,
    "email": "ktlee@gmail.com",
    "password": "$2a$10$XbmeqfL7vQomrf5ewYz5ye8ofLaqWn/8w9ff9NOpehhtQLG7hTqom"
  },
  {
    "doctorID": 32,
    "name": "Dr. Heah Hsin Tak",
    "image": "htheah.png",
    "specialityID": 12,
    "hospitalID": 4,
    "email": "htheah@gmail.com",
    "password": "$2a$10$y8Wj1lnchnGbl1DW/Y7GE.5nmgVWTJwM4tlQaRLbXxDw3she8V95a"
  },
  {
    "doctorID": 33,
    "name": "Dr. Tu Poh Koon",
    "image": "pktu.jpeg",
    "specialityID": 14,
    "hospitalID": 5,
    "email": "pktu@gmail.com",
    "password": "$2a$10$Q9pwUikoBAQEl1aWcDlFC.YaJCnY92UZRrEyfYjvTJA3qVetE/2IW"
  },
  {
    "doctorID": 34,
    "name": "Dr. Khoo Heng Hoon",
    "image": "hhkhoo.png",
    "specialityID": 15,
    "hospitalID": 5,
    "email": "hhkhoo@gmail.com",
    "password": "$2a$10$BRWniSwXwFoBy3ZPkfRkcuxUAASuUgM8nNOU75hzv/jTR8lyWGbX6"
  },
  {
    "doctorID": 35,
    "name": "Dr. Shirlynn Francis",
    "image": "shirlynn.png",
    "specialityID": 15,
    "hospitalID": 5,
    "email": "shirlynn@gmail.com",
    "password": "$2a$10$PkyXpkCsTOIFCHr.WgQ3g.klPRn9uRU5rGEPMCER3I0IWrvGivCPW"
  },
];

let medicalRecord = [
  {
    "recordID": 201,
    "datetime": 1717830000,
    "title": "Broke His Left Leg",
    "description": "Fall down from bicycle , Broke his left leg",
    "hospitalID": 5,
    "doctorID": 35,
    "userID": 'MywJLVPqIiX7PGELcQAXuXSIL4C3',
  },
  {
    "recordID": 202,
    "datetime": 1717992000,
    "title": "Broke His Right Leg",
    "description": "Fall down from bicycle , Broke his right leg",
    "hospitalID": 5,
    "doctorID": 35,
    "userID": 'MywJLVPqIiX7PGELcQAXuXSIL4C3',
  },
  {
    "recordID": 203,
    "datetime": 1718445600,
    "title": "Pulmonary Edema",
    "description": "Difficult to breathe",
    "hospitalID": 5,
    "doctorID": 35,
    "userID": 'MywJLVPqIiX7PGELcQAXuXSIL4C3',
  },
  {
    "recordID": 204,
    "datetime": 1718866800,
    "title": "Heart Disease",
    "description": "High cholesterol , Lack of exercise",
    "hospitalID": 5,
    "doctorID": 35,
    "userID": 'MywJLVPqIiX7PGELcQAXuXSIL4C3',
  },
  {
    "recordID": 205,
    "datetime": 1719104400,
    "title": "Extraction of infected tooth",
    "description": "Toothache in lower left molar",
    "hospitalID": 5,
    "doctorID": 35,
    "userID": 'MywJLVPqIiX7PGELcQAXuXSIL4C3',
  },
];

app.get('/', (req, res) => {
    res.send('CallaDoctor API');
});

app.get('/hospital', (req, res) => {
  res.send(hospital);
});

app.get('/speciality', (req, res) => {
  res.send(speciality);
});

app.get('/doctor', (req, res) => {
  res.send(doctors);
});

let doctorIDCounter = 36;

app.post('/doctor/add', async (req, res) => {
  try {
    const { name, specialityID, hospitalID, email } = req.body;

    if (!name || !specialityID || !hospitalID || !email) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    const passwordPlainText = `${name}123`;
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(passwordPlainText, saltRounds);

    const doctorID = doctorIDCounter++;

    const newDoctor = {
      doctorID: doctorID,
      name,
      image: '',
      specialityID: parseInt(specialityID),
      hospitalID: parseInt(hospitalID),
      email,
      password: hashedPassword
    };

    doctors.push(newDoctor);

    res.status(201).json({ doctor: newDoctor });
    createTimeSlots(doctorID)
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/doctor/delete/:doctorID', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);

  const index = doctors.findIndex(doctor => doctor.doctorID === doctorID);

  if (index === -1) {
    return res.status(404).json({ error: 'Doctor not found.' });
  }

  const deletedDoctor = doctors.splice(index, 1);

  res.json(deletedDoctor[0]);
});

app.get('/doctor/get/:doctorID', (req, res) => {
  const doctorID = parseInt(req.params.doctorID, 10);
  const doctor = doctors.find(doc => doc.doctorID === doctorID);

  if (doctor) {
    res.json({ hospitalID: doctor.hospitalID });
  }
});

app.get('/doctor/:hospitalID', (req, res) => {
  const { hospitalID } = req.params;

  // Convert hospitalID to an integer for comparison
  const hospitalIDInt = parseInt(hospitalID, 10);

  if (isNaN(hospitalIDInt)) {
    return res.status(400).json({ error: 'Invalid hospitalID' });
  }

  // Filter doctors based on hospitalID
  const doctorsInHospital = doctors.filter(doctor => doctor.hospitalID === hospitalIDInt);

  if (doctorsInHospital.length === 0) {
    return res.status(404).json({ message: 'No doctors found for the specified hospitalID' });
  }

  res.json({ doctors: doctorsInHospital });
});

app.get('/medicalRecord/:userID', (req, res) => {
  const userID = req.params.userID;
  const userRecords = medicalRecord.filter(record => record.userID === userID);
  res.json(userRecords);
});

app.get('/medicalRecord/doctor/:doctorID', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);
  const doctorRecords = medicalRecord.filter(record => record.doctorID === doctorID);
  res.json(doctorRecords);
});

let medicalRecordCounter = 206;

app.post('/medicalRecord/add', async (req, res) => {
  const { datetime, title, description, hospitalID, doctorID, userID } = req.body;

  // Validate the required fields
  if (!datetime || !title || !description || !hospitalID || !doctorID || !userID) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  const medicalRecordID = medicalRecordCounter++;

  const newRecord = {
    recordID: medicalRecordID,
    datetime: parseInt(datetime),
    title,
    description,
    hospitalID: parseInt(hospitalID),
    doctorID: parseInt(doctorID),
    userID,
  };

  // Add the new record to the array
  medicalRecord.push(newRecord);

  // Send back the new record as a response
  res.status(201).json(newRecord);
});

app.post('/medicalRecord/delete', (req, res) => {
  const { recordID } = req.body;
  medicalRecord = medicalRecord.filter(record => record.recordID !== parseInt(recordID, 10));
  res.status(200).send({ message: "Record deleted successfully" });
});

let users = [];

const csvWriter = createCsvWriter({
  path: 'user.csv',
  header: [
    { id: 'userID', title: 'userID' },
    { id: 'name', title: 'name' },
    { id: 'ic', title: 'IC' } // Added IC to the header
  ],
  append: true // Append mode to avoid overwriting existing data
});

// Read existing users from CSV if it exists
if (fs.existsSync('user.csv')) {
  const csv = fs.readFileSync('user.csv', 'utf8');
  const lines = csv.split('\n').slice(1); // Remove header
  lines.forEach(line => {
    if (line.trim()) {
      const [userID, name, ic] = line.split(','); // Added IC in parsing
      users.push({ userID, name, ic });
    }
  });
}

// POST route to add a new user
app.post('/user', (req, res) => {
  const user = {
    userID: req.body.userID,
    name: req.body.name,
    ic: req.body.ic // Fixed case to match body input
  };

  // Add the new user to the users array
  users.push(user);

  // Write the new user to the CSV file
  csvWriter.writeRecords([user])
    .then(() => {
      console.log('User added to CSV file');
      res.send(user);
    })
    .catch(err => {
      console.error('Error writing to CSV file', err);
      res.status(500).send({ error: 'Internal Server Error' });
    });
});

app.get('/user/get', (req, res) => {
  res.send(users);
})

app.get('/username/:userID', (req, res) => {
  const userID = req.params.userID;
  const user = users.find(u => u.userID == userID);

  if (user) {
    res.send({ name: user.name, ic: user.ic });
  } else {
    res.status(404).send({ error: 'User not found' });
  }
});


// Login route
app.post('/login/admin', async (req, res) => {
  const { email, password } = req.body;

  // Find the hospital admin by email
  const hospitalAdmin = hospital.find(h => h.email === email);
  if (!hospitalAdmin) {
    return res.status(401).send('Invalid email or password');
  }

  // Compare the hashed password with the one in the request
  const match = await bcrypt.compare(password, hospitalAdmin.password);
  if (!match) {
    return res.status(401).send('Invalid email or password');
  }

  res.json({
    hospitalID: hospitalAdmin.hospitalID
  });
});

// Login route for doctors
app.post('/login/doctor', async (req, res) => {
  const { email, password } = req.body;

  // Find the doctor by email
  const doctor = doctors.find(d => d.email === email);
  if (!doctor) {
    return res.status(401).send('Invalid email or password');
  }

  // Compare the hashed password with the one in the request
  const match = await bcrypt.compare(password, doctor.password);
  if (!match) {
    return res.status(401).send('Invalid email or password');
  }

  // Passwords match, login successful
  // Send the doctorID in the response
  res.json({
    doctorID: doctor.doctorID
  });
});

let timeSlots = [];

function createTimeSlots(doctorID) {
  const start = new Date();
  start.setHours(8, 0, 0, 0); // Start at 8 AM
  const end = new Date(start.getFullYear(), 11, 31); // End on December 31
  end.setHours(17, 0, 0, 0); // End at 5 PM

  const minuteInSecs = 15 * 60; // 15 minutes in seconds

  for (let date = new Date(start); date <= end; date.setMinutes(date.getMinutes() + 15)) {
    const slotDate = Math.floor(date.getTime() / 1000); // Convert to Unix timestamp in seconds
    timeSlots.push({
      doctorID: doctorID,
      slotDate: slotDate,
      blockDate: 0
    });
  }
}

function createTimeSlotsForDoctors(startDocID, endDocID) {
  for (let docID = startDocID; docID <= endDocID; docID++) {
    createTimeSlots(docID);
  }
}

// Pre-create time slots for a doctor with ID 21 to 35
createTimeSlotsForDoctors(21, 35);


// Endpoint to get time slots for a given doctorID
app.get('/timeslots/:doctorID', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);
  const filteredTimeSlots = timeSlots.filter(slot => slot.doctorID === doctorID);
  res.send(filteredTimeSlots);
});

// Endpoint to get time slots for a given doctorID and date
// http://localhost:3000/timeslots/21/2024-12-31
app.get('/timeslots/:doctorID/:date', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);
  const dateParam = req.params.date;
  const date = new Date(dateParam);

  // Get current date and time
  const now = new Date();

  // Set the start time to either now or the start of the given date, whichever is later
  const startOfDay = new Date(Math.max(date.setHours(0, 0, 0, 0), now.getTime()));

  // Set the end time to 10:30 PM on the given date
  const endOfDay = new Date(date.setHours(23, 30, 0, 0));

  // Filter time slots for the specified doctorID within the time range and with blockDate of 0
  const filteredTimeSlots = timeSlots.filter(slot =>
    slot.doctorID === doctorID &&
    slot.slotDate >= startOfDay.getTime() / 1000 &&
    slot.slotDate <= endOfDay.getTime() / 1000 &&
    slot.blockDate === 0
  );

  res.send(filteredTimeSlots);
});

// Endpoint to update blockDate for a specific doctor and time
app.post('/timeslots/update/:doctorID/:time', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);
  const time = parseInt(req.params.time);
  const blockDate = parseInt(req.body.blockDate); // Retrieve blockDate from request body

  // Validate blockDate value
  if (blockDate !== 0 && blockDate !== 1) {
    return res.status(400).send("Invalid blockDate value. It must be 0 or 1.");
  }

  const index = timeSlots.findIndex(slot => slot.doctorID === doctorID && slot.slotDate === time);

  if (index !== -1) {
    timeSlots[index].blockDate = blockDate; // Update blockDate based on request body
    res.send(timeSlots[index]);
  } else {
    res.status(404).send("Time slot not found.");
  }
});


let bookingIDCounter = 10001;
const appointments = [];

app.post('/book', (req, res) => {
  let { userID, hospitalID, doctorID, datetime } = req.body;

  hospitalID = parseInt(hospitalID);
  doctorID = parseInt(doctorID);
  datetime = parseInt(datetime);

  const bookID = bookingIDCounter++;

  const appointment = {
    bookID,
    userID,
    hospitalID,
    doctorID,
    datetime,
    status: 0,
  }

  appointments.push(appointment);

  // Validate the presence of required fields
  if ( !userID || !hospitalID || !doctorID || !datetime ) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  // Send a success response
  res.json(appointment);
});

app.get('/appointment', (req, res) => {
  res.send(appointments);
});

app.post('/appointment/delete/:bookID', (req, res) => {
  const bookID = parseInt(req.params.bookID);

  // Find the index of the appointment with the given bookID
  const index = appointments.findIndex(appointment => appointment.bookID === bookID);

  // If the appointment is not found, send an error response
  if (index === -1) {
    return res.status(404).json({ error: 'Appointment not found.' });
  }

  // Remove the appointment from the array
  const deletedAppointment = appointments.splice(index, 1);

  // Send a success response with the deleted appointment
  res.json(deletedAppointment[0]);
});


app.get('/appointment/:userID', (req, res) => {
  const { userID } = req.params;
  const userAppointments = appointments.filter(appointment => appointment.userID === userID);
  res.json(userAppointments);
});

app.get('/appointment/hospital/:hospitalID', (req, res) => {
  const hospitalID = parseInt(req.params.hospitalID);
  const hospitalAppointments = appointments.filter(appointment => appointment.hospitalID === hospitalID);
  res.json(hospitalAppointments);
});

app.get('/appointment/doctor/:doctorID', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);
  const doctorAppointments = appointments.filter(appointment => appointment.doctorID === doctorID);
  res.json(doctorAppointments);
});


app.post('/appointment/approve/:bookID', (req, res) => {
  const { bookID } = req.params;
  const bookIDInt = parseInt(bookID);

  const index = appointments.findIndex(appointment => appointment.bookID === bookIDInt);

  if (index === -1) {
    return res.status(404).json({ error: 'Appointment not found.' });
  }

  appointments[index].status = 1;

  res.json({ message: 'Appointment approved successfully.' });
});

app.post('/appointment/reject/:bookID', (req, res) => {
  const { bookID } = req.params;
  const bookIDInt = parseInt(bookID);

  const index = appointments.findIndex(appointment => appointment.bookID === bookIDInt);

  if (index === -1) {
    return res.status(404).json({ error: 'Appointment not found.' });
  }

  appointments[index].status = -1;

  res.json({ message: 'Appointment rejected successfully.' });
});

let potentialCustomerIDCounter = 200;
const potentialCustomers = [];

app.post('/clinic/form', (req, res) => {
  let { hospitalName, address, phone, email } = req.body;

  const potentialCustomerID = potentialCustomerIDCounter++;

  const potentialCustomer = {
    potentialCustomerID,
    hospitalName,
    address,
    phone,
    email
  }

  potentialCustomers.push(potentialCustomer);

  if ( !hospitalName || !address || !phone || !email ) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  res.json(potentialCustomer);
});

app.get('/potential/customer', (req, res) => {
  res.send(potentialCustomers);
});


const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));