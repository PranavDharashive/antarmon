import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function Dashboard() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }

        const response = await axios.get('/metrics/all', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMetrics(response.data.metrics);
        setLoading(false);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          navigate('/login');
        } else {
          setError(error);
        }
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);

    return () => clearInterval(interval);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }

  return (
    <div className="App">
      <div style={{ position: 'absolute', top: '10px', right: '10px' }}>
        <Link to="/alerts"><button style={{ marginRight: '10px' }}>Manage Alerts</button></Link>
        <Link to="/agents"><button style={{ marginRight: '10px' }}>Manage Agents</button></Link>
        <button onClick={handleLogout}>Logout</button>
      </div>
      <h1>AntarMon Dashboard</h1>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Hostname</th>
            <th>CPU %</th>
            <th>Memory %</th>
            <th>Disk %</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map((metric) => (
            <tr key={metric[0]}>
              <td>{new Date(metric[5]).toLocaleString()}</td>
              <td>{metric[1]}</td>
              <td>{metric[2]}</td>
              <td>{metric[3]}</td>
              <td>{metric[4]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
