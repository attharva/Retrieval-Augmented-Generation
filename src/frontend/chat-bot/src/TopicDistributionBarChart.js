import { BarChart, XAxis, YAxis, Tooltip, Legend, Bar } from 'recharts';

function TopicDistributionBarChart({ conversation }) {
    const topicCounts = {}
    Object.entries(conversation.topic_distribution || {}).forEach(([topic, count]) => {
        if (!topicCounts[topic]) {
            topicCounts[topic] = 0;
        }
        topicCounts[topic] += count;
    });

    const data = Object.entries(topicCounts).map(([topic, count]) => ({ topic, count }));
    return (
        <div style={{ paddingBottom: 0 }}>
            <BarChart width={600} height={300} data={data}>
                <XAxis dataKey="topic" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
        </div>
    );
}

export default TopicDistributionBarChart