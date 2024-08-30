import React from 'react';

interface Experience {
  company: string;
  role: string;
  duration: string;
  description: string;
}

const experiences: Experience[] = [
  {
    company: "Palantir Technologies",
    role: "Forward Deployed Software Engineer",
    duration: "July 2024 - Present",
    description: "Incoming 2025 New Grad."
  },
  {
    company: "Raytheon Technologies",
    role: "Software Engineer",
    duration: "June 2024 - August 2024",
    description: "Further battling software issues in the avionics subdivision."
  },
  {
    company: "Palantir Technologies",
    role: "Forward Deployed Software Engineer",
    duration: "January 2024 - July 2024",
    description: "Closely worked with F50 clients to build and deploy applications integrated with business ops across 250+ locations."
  },
  {
    company: "Iowa State University Honors Program",
    role: "Research Assistant",
    duration: "August 2022 - January 2024",
    description: "Developing and rigorously testing a Stego-detection software used to detect hidden messages in Smartphone images. Working on getting research findings published soon (ETA: End of December 2024)."
  },
  {
    company: "Collins Aerospace",
    role: "Software Engineer",
    duration: "May 2023 - August 2023",
    description: "Worked with Software within Avionics, specifically the Flight Management Systems component."
  },
  {
    company: "Iowa State University - College of Engineering",
    role: "Math + CS Tutor",
    duration: "January 2022 - December 2022",
    description: "Tutored 50+ Students in Multivariable Calculus, Python and OOP in Java."
  },
  {
    company: "NASA - National Aeronautics and Space Administration",
    role: "NASA L'SPACE NPWEE",
    duration: "January 2022 - March 2022",
    description: "Gained experience in process of writing, reviewing, and scoring proposals through lens of a NASA reviewer."
  },
  {
    company: "Iowa State University",
    role: "Coffee Bar Attendant",
    duration: "August 2021 - December 2021",
    description: "Learnt how to make amazing Coffee + Smoothies @MuMarket, improved my customer interaction and sales skills in the process :)"
  }
];

const WorkTimeline: React.FC = () => {
  return (
    <div className="bg-cream text-matte-black rounded-lg shadow-lg p-6 max-h-[60vh] overflow-y-auto">
      {experiences.map((exp, index) => (
        <div key={index} className="mb-6 relative pl-4 border-l-2 border-matte-black">
          <div className="absolute w-3 h-3 bg-matte-black rounded-full -left-[7px] top-1.5"></div>
          <h3 className="text-xl font-semibold">{exp.company}</h3>
          <h4 className="text-lg font-medium">{exp.role}</h4>
          <p className="text-sm text-gray-600 mb-2">{exp.duration}</p>
          <p className="text-gray-700">{exp.description}</p>
        </div>
      ))}
    </div>
  );
};

export default WorkTimeline;