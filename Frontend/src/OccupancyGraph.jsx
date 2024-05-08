import React, { useState } from "react";
import { Scatter } from "react-chartjs-2";
import { Chart as ChartJS, LinearScale, PointElement, Title, Tooltip, Legend } from "chart.js";
import "./OccupancyGraph.css";

ChartJS.register(LinearScale, PointElement, Title, Tooltip, Legend);

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

  const createDataPoints = (start, end) => {
    let points = [];
    for (let i = 0; i < (end - start) * 4; i++) {
      points.push({
        x: i / 4 + start,  // x values are simply calculated by index/4 + start hour
        y: Math.random() // Random data for demonstration, replace with actual data
      });
    }
    return points;
  };

  const data = createDataPoints(hoursByDay[selectedDay].start, hoursByDay[selectedDay].end);

  const chartData = {
    datasets: [{
      label: `Occupancy Rate for ${selectedDay}`,
      data: data,
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
      pointRadius: 6,
    }]
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true
      },
      x: {
        type: 'linear',
        ticks: {
          stepSize: 1,  // Ensure ticks at every hour
          callback: function(value) {
            if (value % 1 === 0) {  // Only display whole numbers (hourly)
              return `${value}:00`;
            }
          }
        }
      }
    },
    plugins: {
      tooltip: {
        enabled: true
      },
      legend: {
        display: true
      }
    },
    responsive: true,
    maintainAspectRatio: false
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
        <Scatter data={chartData} options={options} />
      </div>
    </div>
  );
};

export default OccupancyGraph;