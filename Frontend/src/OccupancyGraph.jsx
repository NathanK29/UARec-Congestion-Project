import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';

const OccupancyGraph = ({ apiUrl }) => {
  const [chartData, setChartData] = useState({});

  const fetchData = async () => {
    try {
      const response = await axios.get(apiUrl);
      const data = response.data; // Assume you get an array of data structured by day and interval
      const transformedData = transformDataForChart(data);
      setChartData(transformedData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
    // Set up an interval to update the data weekly
    const intervalId = setInterval(fetchData, 604800000); // 604800000 ms = 1 week
    return () => clearInterval(intervalId);
  }, []);

  const transformDataForChart = (data) => {
    // Assuming data is an array of objects with each object representing a day of the week
    // and containing an array of values for each 3-hour interval
    return {
      labels: data.map(day => day.label),
      datasets: [{
        label: 'Occupancy Rate',
        data: data.map(day => day.values),
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      }]
    };
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true
      }
    },
    responsive: true,
    maintainAspectRatio: false
  };

  return (
    <div style={{ height: '400px', width: '600px' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default OccupancyGraph;