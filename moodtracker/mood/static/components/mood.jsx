;(function(global){

const TONES = [
    'anger', 
    'fear', 
    'joy', 
    'sadness', 
    'analytical', 
    'confident', 
    'tentative'
];


class MoodChart extends React.Component {
    constructor(props){
        super(props);
        this.state = {

        };
    }

    render() {

        var xAxis = {
            tickFormat: function(d){ return d3.time.format('%x')(new Date(d)) },
            axisLabel: 'Time',
        }

        var yDomain = [0, 10];

        return (
            <NVD3Chart 
                id="chart" 
                type="lineChart" 
                datum={this.props.chart_data}
                margin={{left: 50, right: 50}}
                x="x"
                xAxis={xAxis}
                y="y"
                yDomain={yDomain}
            />
        );
    }
}

class ToneChart extends React.Component {
    constructor(props){
        super(props);
        this.state = {

        };
    }

    render() {

        var xAxis = {
            tickFormat: function(d){ return d3.time.format('%x')(new Date(d)) },
            axisLabel: 'Time',
        }

        var yDomain = [0, 1];

        return (
            <NVD3Chart 
                id="chart" 
                type="lineChart" 
                datum={this.props.chart_data} 
                margin={{left: 50, right: 50}}
                x="x"
                xAxis={xAxis}
                y="y"
                yDomain={yDomain}
            /> 
        );
    }
}

class TonePieChart extends React.Component {
    constructor(props){
        super(props);
        this.state = {

        };
    }

    render() {

        return (
            <NVD3Chart 
                id="chart" 
                type="pieChart" 
                datum={this.props.chart_data} 
                margin={{left: 50, right: 50}}
                x="key"
                y="y"
            /> 
        );
    }
}



class MoodContainer extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            user_id: user_id,
            raw_user_data: [],
            mood_chart_data: [],
            tone_chart_data: [],
            tonePieData: [],
        };
    }

    componentDidMount(){
        this.getMoodData();
    }

    getMoodData(){
        fetch('/moodtracker/get_user_data/?user_id='+this.state.user_id, {
          method: "GET",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cache': 'no-cache'
          },
          credentials: 'include'
        }).then(response => {
            if(response.ok){
                return response.json();
            }
            throw new Error('Network response was not ok.');
        }).then(data => {

            this.setState({ user_data: data }, function(){
                this.processMoodData();
            });
        });
    }

    processMoodData(){

        // Add Data for Mood Chart
        var moodSeries = {
            key: "Mood",
            color: "red",
            values: []
        };

        for (var moodItem in this.state.user_data.mood){
            var item = this.state.user_data.mood[moodItem];
            var timestamp = Date.parse(item.timestamp);
            var mood = item.mood;
            moodSeries.values.push(
                {
                    x: timestamp, 
                    y: mood
                }
            );
        }

        // Add Data for Tone Chart
        var toneDatum = [];
        var tonePieDatum = [];
        for (var tone in TONES){
            var toneSeries = {
                key: TONES[tone],
                values: []
            };

            for (var moodItem in this.state.user_data.mood){
                var item = this.state.user_data.mood[moodItem];
                var timestamp = Date.parse(item.timestamp);
                for (var toneItem in item.tone.document_tone.tones){
                    var toneDocItem = item.tone.document_tone.tones[toneItem];
                    if (toneDocItem.tone_id == TONES[tone]){
                        toneSeries.values.push(
                            {
                                x: timestamp,
                                y: toneDocItem.score
                            }
                        );
                    }
                }
            }

            toneDatum.push(toneSeries);

            tonePieDatum.push({
                key: toneSeries.key,
                y: toneSeries.values.length
            });
        }

        console.log(toneDatum);
        this.setState({ mood_chart_data: [moodSeries], tone_chart_data: toneDatum, tonePieData: tonePieDatum });
    }

    render() {

        var xAxis = {
            tickFormat: function(d){ return d3.time.format('%x')(new Date(d)) },
            axisLabel: 'Time',
        }

        return (
            <div id="moodContainer">
                <h3>Mood vs. Time</h3>
                <MoodChart chart_data={this.state.mood_chart_data} />
                <h3>Tone vs. Time</h3>
                <ToneChart chart_data={this.state.tone_chart_data} />
                <TonePieChart chart_data={this.state.tonePieData} />
            </div>
            
        );
    }
}

ReactDOM.render(
    <MoodContainer />,
    document.getElementById('reactContainer')
);

})(window);