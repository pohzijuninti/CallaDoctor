const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const app = express();
app.use(express.json());

// add body-parser middleware to parse request bodies
app.use(bodyParser.urlencoded({ extended: false }));

const hospital = [
  {
    "hospitalID": 1,
    "name": "Pantai Hospital Penang",
    "image": "pantai.png",
  },
  {
    "hospitalID": 2,
    "name": "Island Hospital Penang",
    "image": "island.jpeg",
  },
  {
    "hospitalID": 3,
    "name": "Gleneagles Hospital Penang",
    "image": "gleneagles.jpeg",
  },
  {
    "hospitalID": 4,
    "name": "Sunway Medical Centre Penang",
    "image": "sunway.jpeg",
  },
  {
    "hospitalID": 5,
    "name": "Penang Adventist Hospital",
    "image": "adventist.jpeg",
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


const doctor = [
  {
    "doctorID": 21,
    "name": "Dr. Lim Guan Choon",
    "image": "drlim.png",
    "specialityID": 11,
    "hospitalID": 1,
  },
  {
    "doctorID": 22,
    "name": "Dr. Wong Choy Hoong",
    "image": "drwong.jpeg",
    "specialityID": 13,
    "hospitalID": 1,
  },
  {
    "doctorID": 23,
    "name": "Dr. Lai Huey Yoke",
    "image": "drlai.jpeg",
    "specialityID": 15,
    "hospitalID": 1,
  },
  {
    "doctorID": 24,
    "name": "Dr. Goh Tiong Meng",
    "image": "drgoh.png",
    "specialityID": 12,
    "hospitalID": 2,
  },
  {
    "doctorID": 25,
    "name": "Dr. Andrew Lim Keat Eu",
    "image": "drandrew.png",
    "specialityID": 13,
    "hospitalID": 2,
  },
{
    "doctorID": 26,
    "name": "Dr. Khor Yek Huan",
    "image": "drkhor.png",
    "specialityID": 14,
    "hospitalID": 2,
  },
  {
    "doctorID": 27,
    "name": "Dr. Jasjit Singh",
    "image": "drjasjit.jpeg",
    "specialityID": 12,
    "hospitalID": 3,
  },
  {
    "doctorID": 28,
    "name": "Dr. Amelia Lim Lay Suan",
    "image": "dramelia.jpeg",
    "specialityID": 13,
    "hospitalID": 3,
  },
  {
    "doctorID": 29,
    "name": "Dr. Chong Yew Thong",
    "image": "drchong.jpeg",
    "specialityID": 14,
    "hospitalID": 3,
  },
  {
    "doctorID": 30,
    "name": "Dr. Khaw Chee Sin",
    "image": "drkhaw.png",
    "specialityID": 11,
    "hospitalID": 4,
  },
  {
    "doctorID": 31,
    "name": "Dr. Lee Kuo Ting",
    "image": "drlee.png",
    "specialityID": 11,
    "hospitalID": 4,
  },
  {
    "doctorID": 32,
    "name": "Dr. Heah Hsin Tak",
    "image": "drheah.png",
    "specialityID": 12,
    "hospitalID": 4,
  },
  {
    "doctorID": 33,
    "name": "Dr. Tu Poh Koon",
    "image": "drtu.jpeg",
    "specialityID": 14,
    "hospitalID": 5,
  },
  {
    "doctorID": 34,
    "name": "Dr. Khoo Heng Hoon",
    "image": "drkhoo.png",
    "specialityID": 15,
    "hospitalID": 5,
  },
  {
    "doctorID": 35,
    "name": "Dr. Shirlynn Francis",
    "image": "drshirlynn.png",
    "specialityID": 15,
    "hospitalID": 5,
  },
];

const description = [
  {
    "descriptionID": 201,
    "datetime": 1717830000,
    "caution": "High blood pressure",
    "description": "Routine checkup for heart condition",
    "userID": 101,
  },
  {
    "descriptionID": 202,
    "datetime": 1717992000,
    "caution": "Appendicitis",
    "description": "Surgery scheduled for appendectomy",
    "userID": 102,
  },
  {
    "descriptionID": 203,
    "datetime": 1718445600,
    "caution": "Vision blurry in right eye",
    "description": "Consultation for possible cataracts",
    "userID": 103,
  },
  {
    "descriptionID": 204,
    "datetime": 1718866800,
    "caution": "Eczema flare-up",
    "description": "Prescription refill for eczema cream",
    "userID": 104,
  },
  {
    "descriptionID": 205,
    "datetime": 1719104400,
    "caution": "Toothache in lower left molar",
    "description": "Extraction of infected tooth",
    "userID": 105,
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
  res.send(doctor);
});

app.get('/description', (req, res) => {
  res.send(description);
});

let users = [];

const csvWriter = createCsvWriter({
  path: 'user.csv',
  header: [
    { id: 'userID', title: 'userID' },
    { id: 'name', title: 'name' }
  ],
  append: true // Append mode to avoid overwriting existing data
});

if (fs.existsSync('user.csv')) {
  const csv = fs.readFileSync('user.csv', 'utf8');
  const lines = csv.split('\n').slice(1); // Remove header
  lines.forEach(line => {
    if (line) {
      const [userID, name] = line.split(',');
      users.push({ userID, name });
    }
  });
}

app.post('/user', (req, res) => {
  const user = {
      userID: req.body.userID,
      name: req.body.name,
  };
  users.push(user);
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

app.get('/username/:userID', (req, res) => {
  const userID = req.params.userID;
  const user = users.find(u => u.userID == userID);

  if (user) {
    res.send({ name: user.name });
  } else {
    res.status(404).send({ error: 'User not found' });
  }
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
  const startOfDay = new Date(Math.max(date.setHours(0, 0, 0, 0), now.setHours(now.getHours(), now.getMinutes(), 0, 0)));
  // Set the end time to 10:30 PM on the given date
  const endOfDay = new Date(date.setHours(22, 30, 0, 0));
  // Filter time slots for the specified doctorID within the time range
  const filteredTimeSlots = timeSlots.filter(slot => slot.doctorID === doctorID && slot.slotDate >= startOfDay.getTime() / 1000 && slot.slotDate <= endOfDay.getTime() / 1000);
  res.send(filteredTimeSlots);
});

// Endpoint to update blockDate for a specific doctor and time
app.post('/timeslots/:doctorID/:time', (req, res) => {
  const doctorID = parseInt(req.params.doctorID);
  const time = parseInt(req.params.time);
  const index = timeSlots.findIndex(slot => slot.doctorID === doctorID && slot.slotDate === time);
  if (index !== -1) {
    timeSlots[index].blockDate = 1;
    res.send(timeSlots[index]);
  } else {
    res.status(404).send("Time slot not found.");
  }
});

let bookingIDCounter = 10001;
const appointments = [];

app.post('/book', (req, res) => {
  let { userID, locationID, docID, datetime } = req.body;

  locationID = parseInt(locationID);
  docID = parseInt(docID);
  datetime = parseInt(datetime);

  const bookID = bookingIDCounter++;

  const appointment = {
    bookID,
    userID,
    locationID,
    docID,
    datetime,
  }

  appointments.push(appointment);

  // Validate the presence of required fields
  if ( !userID || !locationID || !docID || !datetime ) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  // Send a success response
  res.json(appointment);
});


app.get('/appointment', (req, res) => {
  res.send(appointments);
});

app.get('/appointment/:userID', (req, res) => {
  const { userID } = req.params;

  // Find appointments for the given userID
  const userAppointments = appointments.filter(appointment => appointment.userID === userID);

  // Send the filtered list of appointments
  res.json(userAppointments);
});

// Delete an appointment by bookID using POST method
app.post('/appointment/delete/:bookID', (req, res) => {
  const { bookID } = req.params;
  const bookIDInt = parseInt(bookID);

  // Find the index of the appointment to be deleted
  const index = appointments.findIndex(appointment => appointment.bookID === bookIDInt);

  if (index === -1) {
    return res.status(404).json({ error: 'Appointment not found.' });
  }

  // Remove the appointment from the array
  appointments.splice(index, 1);

  // Send a success response
  res.json({ message: 'Appointment deleted successfully.' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));