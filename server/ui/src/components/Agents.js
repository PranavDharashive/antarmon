import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Agents() {
  const [agents, setAgents] = useState([]);
  const [agentName, setAgentName] = useState('');
  const [newApiKey, setNewApiKey] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/agents', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setAgents(response.data.agents);
      } catch (error) {
        setError('Failed to fetch agents');
      }
    };

    fetchAgents();
  }, []);

  const handleRegisterAgent = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/agents', { name: agentName }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setNewApiKey(response.data.api_key);
      setAgentName('');
      // Refresh the agents list
      const updatedAgents = await axios.get('/agents', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAgents(updatedAgents.data.agents);
    } catch (error) {
      setError('Failed to register agent');
    }
  };

  return (
    <div>
      <h2>Manage Agents</h2>
      
      <h3>Register New Agent</h3>
      <form onSubmit={handleRegisterAgent}>
        <input 
          type="text" 
          value={agentName} 
          onChange={(e) => setAgentName(e.target.value)} 
          placeholder="Agent Name" 
          required 
        />
        <button type="submit">Register</button>
      </form>
      {newApiKey && (
        <div>
          <h4>New API Key:</h4>
          <p>Please save this key. You will not be able to see it again.</p>
          <code>{newApiKey}</code>
        </div>
      )}

      <h3>Your Agents</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>API Key</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((agent) => (
            <tr key={agent[0]}>
              <td>{agent[0]}</td>
              <td>{agent[1]}</td>
              <td>{agent[2]}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Agents;
