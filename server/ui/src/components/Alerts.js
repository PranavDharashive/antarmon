import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [metricName, setMetricName] = useState('cpu_percent');
  const [threshold, setThreshold] = useState('');
  const [error, setError] = useState('');

  const fetchAlerts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/alerts', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAlerts(response.data.alerts);
    } catch (error) {
      setError('Failed to fetch alerts');
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleCreateAlert = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await axios.post('/alerts', { metric_name: metricName, threshold: parseFloat(threshold) }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMetricName('cpu_percent');
      setThreshold('');
      fetchAlerts(); // Refresh the alerts list
    } catch (error) {
      setError('Failed to create alert');
    }
  };

  const handleDeleteAlert = async (alertId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/alerts/${alertId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchAlerts(); // Refresh the alerts list
    } catch (error) {
      setError('Failed to delete alert');
    }
  };

  return (
    <div>
      <h2>Manage Alerts</h2>
      
      <h3>Create New Alert</h3>
      <form onSubmit={handleCreateAlert}>
        <select value={metricName} onChange={(e) => setMetricName(e.target.value)}>
          <option value="cpu_percent">CPU Percent</option>
          <option value="memory_percent">Memory Percent</option>
          <option value="disk_percent">Disk Percent</option>
        </select>
        <input 
          type="number" 
          value={threshold} 
          onChange={(e) => setThreshold(e.target.value)} 
          placeholder="Threshold (%)" 
          required 
        />
        <button type="submit">Create</button>
      </form>

      <h3>Your Alerts</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Metric Name</th>
            <th>Threshold</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert[0]}>
              <td>{alert[0]}</td>
              <td>{alert[1]}</td>
              <td>{alert[2]}%</td>
              <td><button onClick={() => handleDeleteAlert(alert[0])}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Alerts;
