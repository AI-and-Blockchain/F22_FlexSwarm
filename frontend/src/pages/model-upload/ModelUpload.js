import React, {useState, useContext, useEffect, Suspense} from 'react';
import { useNavigate } from 'react-router-dom';
import "./ModelUpload.css";
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Select from 'react-select';

// {'plane': 0,
//  'car': 1,
//  'bird': 2,
//  'cat': 3,
//  'deer': 4,
//  'dog': 5,
//  'frog': 6,
//  'horse': 7,
//  'ship': 8,
//  'truck': 9,
//  'other': -1}
const labels = [
  { value: 'plane', label: 'Plane' },
  { value: 'car',   label: 'Car' },
  { value: 'bird',  label: 'Bird' },
  { value: 'car',   label: 'Cat' },
  { value: 'deer',  label: 'Deer' },
  { value: 'dog',   label: 'Dog' },
  { value: 'frog',  label: 'Frog' },
  { value: 'horse', label: 'Horse' },
  { value: 'ship',  label: 'Ship' },
  { value: 'truck', label: 'Truck' },
  { value: 'other', label: 'Others' }
];

const model_components = [
  { value: 'BatchNorm1d', label: 'BatchNorm1d' },
  { value: 'Linear', label: 'Linear' },
  { value: 'Conv2D', label: 'Conv2D' },
  { value: 'ReLU', label: 'ReLU' },
  { value: 'Sigmoid', label: 'Sigmoid' },
  { value: 'MaxPool', label: 'MaxPool' },
  { value: 'AveragePooling', label: 'AveragePooling' },
  { value: 'Flatten', label: 'Flatten' },
  { value: 'Softmax', label: 'Softmax' },
]


const ModelUpload = () => {

  const [submitted, setSubmitted] = useState(false);

  const [selectedOption, setSelectedOption] = useState(null);

  // const modelEval = () => {

  // }

  return (
    <div className="ModelUpload">
      {
        !submitted ? 
        <>
          <Form id='modelConfig'>
            <Form.Group className="mb-3 " controlId="formBasicEmail">
              <Form.Label>Labels</Form.Label>
              <Select 
              defaultValue={selectedOption}
              onChange={setSelectedOption}
              options={labels}
              isMulti={true}
              />
            </Form.Group>

            <Form.Group className="mb-3 " controlId="formBasicEmail">
              <Form.Label>HyperParams</Form.Label>
              <Form.Control placeholder="lr=0.001 | loss=Adam"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Model Structure</Form.Label>
              <div>Layer</div>
              <Select 
                defaultValue={selectedOption}
                onChange={setSelectedOption}
                options={model_components}
                isMulti={false}
              />
              <div>Param</div>
              <Form.Control placeholder="BatchNorm1d(768, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)"/>
              <div>Layer</div>
              <Select 
                defaultValue={selectedOption}
                onChange={setSelectedOption}
                options={model_components}
                isMulti={false}
              />
              <div>Param</div>
              <Form.Control placeholder="Linear(in_features=768, out_features=128, bias=True)"/>
              <div>Layer</div>
              <Select 
                defaultValue={selectedOption}
                onChange={setSelectedOption}
                options={model_components}
                isMulti={false}
              />
              <div>Param</div>
              <Form.Control placeholder="GELU"/>
              <div>Layer</div>
              <Select 
                defaultValue={selectedOption}
                onChange={setSelectedOption}
                options={model_components}
                isMulti={false}
              />
              <div>Param</div>
              <Form.Control placeholder="Linear(in_features=128, out_features=3, bias=True)"/>
            </Form.Group>

            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Upload Model (*.pt)</Form.Label>
              <Form.Control type="file" />
            </Form.Group>

            <Button variant="primary" type="submit" onClick={() => {setSubmitted(true)}}>
              Upload
            </Button>
          </Form>
        </>
        :
        <>
          
          <div>
            {() => {setTimeout(10, "Accepted: 87.734%") }}
          </div>
        </>
      }
      
    </div>
  )
}

export default ModelUpload;

