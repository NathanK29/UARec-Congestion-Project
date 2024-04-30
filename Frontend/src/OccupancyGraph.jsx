import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import "./OccupancyGraph.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const hoursByDay = {
  Monday: { start: 6, end: 24 },
  Tuesday: { start: 6, end: 24 },
  Wednesday: { start: 6, end: 24 },
  Thursday: { start: 6, end: 24 },
  Friday: { start: 6, end: 23 },
  Saturday: { start: 8, end: 23 },
  Sunday: { start: 8, end: 24 },
};

const OccupancyGraph = () => {
  const currentDayIndex = new Date().getDay() - 1;
  const defaultDay = days[currentDayIndex === -1 ? 6 : currentDayIndex];

  const [selectedDay, setSelectedDay] = useState(defaultDay);

  const createLabels = (start, end) => {
    return Array.from({ length: end - start }, (_, i) => {
      const hour = start + i;
      const hour12 = hour % 12 === 0 ? 12 : hour % 12; // Convert 0 to 12 for 12-hour format
      const amPm = hour < 12 ? "AM" : "PM"; // Determine AM/PM based on 24-hour time
      return `${hour12}:00 ${amPm}`; // Format the string
    });
  };

  // Example data structure for each day
  const hourlyData = {
    Monday: [0.5, 0.2, 0.05, 0.05, 0.05, 0.2, 0.5, 0.8, 1.3, 1.7, 2.2, 2.7, 3.2, 3.6, 4, 4.2, 4.5, 4.59],
    Tuesday: [0.6, 0.2, 0.05, 0.05, 0.05, 0.2, 0.5, 1, 1.5, 2.2, 2.6, 3.2, 3.5, 3.7, 3.7, 3.4, 3.2, 2.5],
    Wednesday: [0.6, 0.2, 0.05, 0.05, 0.05, 0.2, 0.5, 0.8, 1.5, 1.8, 2.4, 2.7, 3.15, 3.2, 3.2, 3, 2.5, 1.5],
    Thursday: [0.5, 0.2, 0.05, 0.05, 0.2, 0.5, 0.6, 0.8, 1.3, 1.6, 2.1, 2.4, 2.7, 3.1, 3.2, 3.55, 3.65, 3.55],
    Friday: [0.5, 0.2, 0.05, 0.2, 0.3, 0.6, 1, 1.5, 2.1, 2.5, 3, 3.3, 3.4, 3.3, 2.9, 2.3, 1.5],
    Saturday: [0.5, 1.2, 2, 2.5, 2.9, 3, 3.1, 3.05, 3, 2.9, 2.8, 2.6, 2.4, 2.3, 2.3],
    Sunday: [0.3, 1.2, 1.9, 2.5, 2.9, 3, 3.1, 3, 2.9, 2.8, 2.7, 2.6, 2.4, 2.3, 2.25],
  };

  const labels = createLabels(hoursByDay[selectedDay].start, hoursByDay[selectedDay].end);
  const data = hourlyData[selectedDay];

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: `Occupancy Rate for ${selectedDay}`,
        data: data,
        backgroundColor: "rgba(53, 162, 235, 0.5)",
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          display: false,
        },
        grid: {
          drawBorder: true,
          //display: false
        },
      },
      x: {
        grid: {
          //display: false
        },
      },
    },
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: function (context) {
            const value = context.raw;
            if (value >= 0 && value <= 2.0) {
              return `Usually not too busy`;
            } else if (value > 2.0 && value <= 3) {
              return `Moderately busy ${value}`;
            } else {
              return `Very busy`;
            }
          },
        },
      },
      legend: {
        display: true,
      },
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div>
      <select className="selector" value={selectedDay} onChange={(e) => setSelectedDay(e.target.value)}>
        {days.map((day) => (
          <option key={day} value={day}>
            {day}
          </option>
        ))}
      </select>
      <div className="graph-container">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  );
};

console.log(ChartJS.version);

export default OccupancyGraph;
