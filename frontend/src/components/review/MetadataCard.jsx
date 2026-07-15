export default function MetadataCard({ metadata }) {

    if (!metadata) return null;

    return (

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">

            <h2 className="text-2xl font-bold mb-6">
                Project Information
            </h2>

            <div className="grid md:grid-cols-3 gap-6">

                <div>
                    <p className="text-slate-400">
                        Project Name
                    </p>

                    <p className="font-semibold text-lg">
                        {metadata.project_name}
                    </p>
                </div>

                <div>
                    <p className="text-slate-400">
                        Generated At
                    </p>

                    <p className="font-semibold">
                        {metadata.generated_at}
                    </p>
                </div>

                <div>
                    <p className="text-slate-400">
                        Report Version
                    </p>

                    <p className="font-semibold">
                        {metadata.report_version}
                    </p>
                </div>

                <div>
                    <p className="text-slate-400">
                        Total Files
                    </p>

                    <p className="text-3xl font-bold">
                        {metadata.total_files}
                    </p>
                </div>

                <div>
                    <p className="text-slate-400">
                        Total Lines
                    </p>

                    <p className="text-3xl font-bold">
                        {metadata.total_lines}
                    </p>
                </div>

                <div>
                    <p className="text-slate-400">
                        Average Score
                    </p>

                    <p className="text-3xl font-bold text-green-400">
                        {metadata.average_score}
                    </p>
                </div>

            </div>

        </div>

    );

}