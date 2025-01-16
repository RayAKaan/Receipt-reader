import React, { useEffect, useState } from 'react';

const ReceiptViewer = ({ match }) => {
  const [receipt, setReceipt] = useState(null);

  useEffect(() => {
    fetch(`/api/receipt/${match.params.id}`)
      .then((res) => res.json())
      .then((data) => setReceipt(data));
  }, [match.params.id]);

  if (!receipt) return <div>Loading...</div>;

  return (
    <div>
      <h2>Receipt Details</h2>
      <p>Filename: {receipt.filename}</p>
      <p>Total Expense: {receipt.total_expense}</p>
    </div>
  );
};

export default ReceiptViewer;
