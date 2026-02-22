import React, { useState } from 'react';
import { generateRoadmap } from '../api';
import { CheckCircle, Circle, ArrowRight } from 'lucide-react';

const RoadmapView = ({ department }) => {
    const [roadmap, setRoadmap] = useState(null);
    const [level, setLevel] = useState('Beginner');
    const [loading, setLoading] = useState(false);

    const handleGenerate = async () => {
        setLoading(true);
        const data = await generateRoadmap(department, level);
        setRoadmap(data);
        setLoading(false);
    };

    return (
        <div className="h-full overflow-y-auto bg-gray-50">
            <div className="p-8 max-w-4xl mx-auto">
                <div className="mb-8 text-center">
                    <h2 className="text-3xl font-bold text-gray-800 mb-2">{department} Learning Path</h2>
                    <p className="text-gray-500">Structured curriculum from zero to hero</p>
                </div>

                {/* Controls */}
                <div className="flex justify-center gap-4 mb-12">
                    {['Beginner', 'Intermediate', 'Advanced'].map((lvl) => (
                        <button
                            key={lvl}
                            onClick={() => setLevel(lvl)}
                            className={`px-6 py-2 rounded-full text-sm font-medium transition-all ${level === lvl
                                ? 'bg-indigo-600 text-white shadow-lg transform scale-105'
                                : 'bg-white text-gray-600 border border-gray-200 hover:border-indigo-300'
                                }`}
                        >
                            {lvl}
                        </button>
                    ))}
                    <button
                        onClick={handleGenerate}
                        disabled={loading}
                        className="ml-4 px-6 py-2 bg-green-600 text-white rounded-full font-bold shadow-md hover:bg-green-700 transition-colors"
                    >
                        {loading ? 'Designing...' : 'Generate Roadmap'}
                    </button>
                </div>

                {/* Timeline */}
                {roadmap && (
                    <div className="space-y-8 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-300 before:to-transparent">
                        {roadmap.modules.map((module, index) => (
                            <div key={index} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                                {/* Icon */}
                                <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-indigo-50 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                                    <CheckCircle className="w-5 h-5 text-indigo-600" />
                                </div>
                                {/* Card */}
                                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-6 rounded-2xl shadow-sm border border-gray-100 transition-all hover:shadow-md">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-xs font-bold text-indigo-500 uppercase tracking-wider">Week {module.week}</span>
                                        <span className="text-xs text-gray-400">2-4 Hours</span>
                                    </div>
                                    <h3 className="text-lg font-bold text-gray-800 mb-2">{module.topic}</h3>
                                    <p className="text-gray-600 text-sm mb-4 leading-relaxed">{module.description}</p>

                                    {module.resources && (
                                        <div className="bg-gray-50 rounded-lg p-3">
                                            <h4 className="text-xs font-semibold text-gray-500 mb-2 uppercase">Recommended Resources</h4>
                                            <ul className="space-y-2">
                                                {module.resources.map((res, i) => (
                                                    <li key={i}>
                                                        <a href={res.link} target="_blank" rel="noopener noreferrer" className="flex items-center text-sm text-indigo-600 hover:underline">
                                                            <ArrowRight className="w-3 h-3 mr-2" />
                                                            {res.title}
                                                        </a>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default RoadmapView;
