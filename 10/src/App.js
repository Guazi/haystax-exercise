import React, { Component } from 'react';
import logo from './logo.svg';
import { Row, Col, Layout, Card, List } from 'antd';
import { Input } from 'antd';

import './App.css';
const Search = Input.Search;
const { Header, Content, Footer, Sider } = Layout;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: ''
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange = event => {
    const api = 'http://localhost:4002/twitter?handle=';
    fetch(api + event)
    // Return the results as json
      .then(results => results.json())
      // Map the data to the state variable datum
      .then(data => {
        this.setState({ datum: data });
        console.log('singlestate', this.state.datum);
      })
      // Catch error, usually handle was not valid.  Set datum to empty
      .catch(error => {
        console.log(error);
        this.setState({ datum: '' });
      });
    console.log(event);
    this.setState({ value: event }, console.log(this.state));
  };

  render() {
    return (
      <div className="App">
      <div> <img className="logo" src="/logo.png"/></div>
        <Content style={{ padding: '5vh 10vw' }}>
          <Row>
            <Col span={24}>
              <Search placeholder="Enter Twitter Handle @" onSearch={this.handleChange} enterButton/>
            </Col>
          </Row>
          {/* The user has entered in a twitter handle, show them we are processing the data. */}
          {this.state.value.length > 0
            && <Row>
              <Col span={24}>
                <h4 className="m10-0">Last Five Tweets for Twitter User: {`@${this.state.value}`}</h4>
              </Col>
            </Row>
          }
          {/* The call to the twitter API was successfull (handle was valid) and returned data */}
          {this.state.datum
            && <div>
                <List
                  grid={{ gutter: 18, xs: 1, sm: 1, md: 2, lg: 2, xl: 3, xxl: 3 }}
                  dataSource={this.state.datum}
                  renderItem={item =>
                    <List.Item>
                      <Card  >
                      <p className="title-height">{item.full_text}</p>
                      <p> Tweeted on: {item.date} EST</p>
                      <p> There are {item.totalwords} total words in this tweet. Of those {item.totalwords} total words, there are {item.english} ({item.percentenglish}%) that are in English.</p>

                      </Card>
                    </List.Item>
                  }
                />
            </div>
          }
        </Content>
      </div>
    );
  }
}

export default App;
