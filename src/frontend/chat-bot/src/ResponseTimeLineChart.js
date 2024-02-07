import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

function ResponseTimeLineChart({ conversationHistory }) {
  const data = conversationHistory.map((entry, index) => ({
    name: `Q${index + 1}`,
    duration: entry.duration,
  }));

  return (
    <div style={{ paddingBottom: 0 }}>
      <LineChart width={600} height={350} data={data} style={{paddingBottom: 10}}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" label={{ value: 'Queries', offset: -8, position: 'bottom' }} />
        <YAxis label={{ value: 'Response Time (seconds)', angle: -90 }} />
        <Tooltip />
        <Line type="monotone" dataKey="duration" stroke="#8884d8" />
      </LineChart>
    </div>
  );
}

export default ResponseTimeLineChart