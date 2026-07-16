import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid
} from "recharts";

const COLORS = [
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#3b82f6"
];

export default function AnalyticsCharts({ dashboard }) {

    if (!dashboard) return null;

    const severityData = [
        {
            name: "Critical",
            value: dashboard.critical
        },
        {
            name: "High",
            value: dashboard.high
        },
        {
            name: "Medium",
            value: dashboard.medium
        },
        {
            name: "Low",
            value: dashboard.low
        }
    ];

    const fileData = [
        {
            name: "Passed",
            value: dashboard.passed_files
        },
        {
            name: "Failed",
            value: dashboard.failed_files
        }
    ];

    return (

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            <div className="bg-slate-900 rounded-xl border border-slate-800 p-6">

                <h3 className="text-xl font-bold text-white mb-5">
                    AI Severity Distribution
                </h3>

                <ResponsiveContainer width="100%" height={300}>

                    <PieChart>

                        <Pie
                            data={severityData}
                            dataKey="value"
                            outerRadius={100}
                        >

                            {severityData.map((entry, index) => (

                                <Cell
                                    key={index}
                                    fill={COLORS[index]}
                                />

                            ))}

                        </Pie>

                        <Tooltip />

                    </PieChart>

                </ResponsiveContainer>

            </div>

            <div className="bg-slate-900 rounded-xl border border-slate-800 p-6">

                <h3 className="text-xl font-bold text-white mb-5">
                    Passed vs Failed Files
                </h3>

                <ResponsiveContainer width="100%" height={300}>

                    <BarChart data={fileData}>

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="name" />

                        <YAxis />

                        <Tooltip />

                        <Bar
                            dataKey="value"
                            fill="#22c55e"
                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

        </div>

    );

}