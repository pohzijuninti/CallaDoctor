const express = require('express');
const app = express();
const bodyParser = require('body-parser');

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

app.use(express.json());

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

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));