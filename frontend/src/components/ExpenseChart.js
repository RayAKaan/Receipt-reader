import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const ExpenseChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/receipts')
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  const chartData = {
    x: data.map((item) => item.filename),
    y: data.map((item) => item.total_expense),
    type: 'bar',
    marker: { color: 'blue' },
  };

  return (
    <div>
      <h2>Expense Chart</h2>
      <Plot data={[chartData]} layout={{ title: 'Expenses' }} />
    </div>
  );
};

export default ExpenseChart;
