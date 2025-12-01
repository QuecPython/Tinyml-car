# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import utime
import math
import log
try:
    from random_forest import RandomForest
except ImportError:
    from usr.random_forest import RandomForest


log.basicConfig(level=log.INFO)
tinyml_log = log.getLogger("TinyML")

class TinyML_Utils:

    @classmethod
    def get_time(cls) -> int:
        '''
            Gets current time in ms format. 
        '''
        return utime.mktime(utime.localtime()) * 1000
    
    @classmethod
    def get_time_diff(cls, inference_tuples: list) -> int:
        '''
            Calculates the time difference between the first and last 
            inference in a list of inference tuples.
        
            Args:
                inference_tuples: List of tuples containing time and inference data.
            Returns:
                Time difference between first and last inference.
        '''
        if len(inference_tuples) >= 2:
            return utime.ticks_diff(inference_tuples[-1][0], inference_tuples[0][0])
        else:
            return 0      

    @classmethod
    def get_final_inf_res(cls, infs: list) -> int:
        '''
            Gets the most frequent inference result in a list of inferences.

            Args:
                infs: List of inference results.   
            Returns:
                Returns the most frequent value in a list.
        '''
        return max(set(infs), key=infs.count)
    
    @classmethod
    def reduce_infs(cls, inference_tuples: list, min_tuples: int) -> list:
        '''
            Returns the first defined number of inferences in a list inference tuples.
            
            Args:
                inference_tuples: List of inference tuples. Format of tuple `(time, inference).`
                min_tuples: Number of inferences to return from list of tuples.
            Returns:
                List of first n inferences.
        '''
        return [x[1] for x in inference_tuples[:min_tuples]]

    @classmethod
    def debounce(cls, inference_tuples: list, time_diff: int, 
                 min_tuples: int, min_t_diff: int) -> int:
        '''
            Debounces inferences - returns the most prevalent
            score from the collected inference results.
            
            Args:
                inference_tuples: List of inference tuples. Format `(time,inference)`.
                time_diff: Difference between first and last inference in a list.
                min_tuples: Number of inferences to return from list of tuples.
                min_t_diff: Min. time difference between first and last inference.
            Returns:
                result: Most prevalent inference result.
                reduced_infs: List of first n collected inference values.
        '''
        if len(inference_tuples) >= min_tuples and time_diff > min_t_diff:
            reduced_infs = cls.reduce_infs(inference_tuples, min_tuples)
            result = cls.get_final_inf_res(reduced_infs)
            # print('{} -> {}'.format(reduced_infs, result))
            return result
        else:
            return None

    @classmethod
    def clean_inf_tuples(cls, inference_tuples: list, time_diff: int,
                         max_tuples: int, max_t_diff: int) -> list:
        '''
            Purges inference tuples buffer.
            
            Args:
                inference_tuples: List of inference tuples. Format `(time,inference)`.
                time_diff: Difference between first and last inference in a list.
            Returns:
                List of inference tuples.
        '''
        if len(inference_tuples) <= max_tuples and time_diff >= max_t_diff:
            print("Cleaning inference tuples")
            return []
        else:
            return inference_tuples


class TinyML:
    '''
        Class to process data collected from accelerometer.
        
        Attributes:
            n_signals: Number of unique signals that will be stored.
            capacity: Calculated capacity needed to have 1 second of signal data.
            buffer: Collected data is stored in buffer.
    '''
    class __Config_:
        TIME_DIFF=450 # MS -Adapted to Circular Movement (450ms)
        MIN_INF_TUPLES=3 # 3 consecutive results (150ms with 50MS interval)

        CLEAN_MAX_TUPLES=8
        CLEAN_MAX_TIME_DIFF=2000 # ms

    def __init__(self, freq, n_signals):
        '''Initializes Data class with `n_signals`,`capacity`, `buffer`.'''
        self.n_signals = n_signals
        self.capacity = freq * self.n_signals
        # self.capacity = (freq * self.n_signals) + self.n_signals
        self.buffer = []

        # initialize inference collection tuples
        self.inference_tuples = []

    def get_size(self) -> int:
        '''Returns the size of the collected data buffer.'''
        return len(self.buffer)

    def get_capacity(self) -> int:
        '''Returns the capacity of Data class.'''
        return self.capacity

    def get_data(self) -> list:
        '''Returns collected data.'''
        return self.buffer

    def scale(self, vals: list, xmin: int, xmax: int, f_range: int) -> list:
        '''
            Rescales data from 0 to defined value.
            
            Args:
                vals: List of values to rescale.
                xmin: Min value refernce.
                xmax: Max value reference.
                f_range: Feature range from 0 to defined value.
            Returns:
                List of scales values.
        '''
        return [int((x-xmin)/(xmax-xmin)*f_range) for x in vals]

    def round(self, vals: list, places: int=4) -> list:
        '''
            Rounds float values int a list to defined decimal points.
            
            Args:
                vals: List of values to round.
                places: Number of decimal places for rounding.   
            Returns:
                List of rounded floats.
        '''
        return [round(x, places) for x in vals]

    def is_full(self) -> bool:
        '''
            Verifies if buffer has capacity to add new values.
            (self.capacity - self.n_signals) - number of signals must be 
            subtracted as new values will be added after check.
            
            Returns:
                True if buffer is larger than capacity - # of signals
        '''
        return len(self.buffer) >= self.capacity
 

    def update_config(self, time_diff = __Config_.TIME_DIFF,
                       min_inf_tuples = __Config_.MIN_INF_TUPLES, 
                       clean_max_tuples = __Config_.CLEAN_MAX_TUPLES, 
                       clean_max_time_diff = __Config_.CLEAN_MAX_TIME_DIFF) -> None:
        TinyML.__Config_.TIME_DIFF = time_diff
        TinyML.__Config_.MIN_INF_TUPLES = min_inf_tuples
        TinyML.__Config_.CLEAN_MAX_TUPLES = clean_max_tuples
        TinyML.__Config_.CLEAN_MAX_TIME_DIFF = clean_max_time_diff

    def get_rms(self, signal: int) -> float:
        '''
            Gets root mean square (RMS) of defined signal.
            
            Args:
                signal: Number of signal in order as collected.
                        Depends on how signals are defined in `collect` method.
                        Given `Data.collect([acc_x, acc_y],[gyro_x])` and 
                        `get_rms(1)` - this method will return the RMS of `acc_y`.
            Returns:
                RMS of a signal.
        '''
        vals = self.buffer[signal:][0::3]
        
        '''
            Calculates the root mean square of a signal.
            
            Args:
                vals: List of ints or floats.
            Returns:
                Root mean square of input values.
        '''
        pow = math.pow # method preloading for speedup
        l = len(vals)
        res = math.sqrt(sum([pow(x,2) for x in vals]) / l)

        return res

    def collect(self, acc: list=None, gyro:list=None) -> None:
        '''
            Collects and regulates data in buffer.
            
            Args:
                acc: List of acceleration sensor reading values.
                gyro: List of gyroscope sensor reading values.
        '''
        # Count total new values
        new_values_count = 0
        if acc:
            new_values_count += len(acc)
        if gyro:
            new_values_count += len(gyro)
        
        # Remove old values to make room for new ones
        while len(self.buffer) + new_values_count > self.capacity:
            self.buffer.pop(0)
        
        # Add new values
        if acc:
            self.buffer.extend(acc)
        if gyro:
            self.buffer.extend(gyro)

    def score(self) -> int:
        '''
        Runs scoring on collected data, return result.
        '''
        now = utime.ticks_ms()

        if len(self.buffer) == self.capacity:
            res = RandomForest.run(self.buffer)+1
            # print("推理结果:", res)
            if res in [1,2,3,4]:
                self.inference_tuples.append((now, res))
                #print("Added to inference_tuples. Total:", len(self.inference_tuples))
            else:
                #print("Result 0 ignored (no gesture)")
                pass
        
        time_diff = TinyML_Utils.get_time_diff(self.inference_tuples)
        # print("Inference tuples:", len(self.inference_tuples), "Time diff:", time_diff)

        ''' 
        # Agresivno čišćenje - obriši listu ako je stara više od 1000ms od prvog rezultata
        if len(self.inference_tuples) > 0:
            first_result_time = self.inference_tuples[0][0]
            time_since_first = utime.ticks_diff(now, first_result_time)
            if time_since_first >= 1000:
                print("Clearing old inference data (1000ms timeout from first result)")
                self.inference_tuples = []
                time_diff = 0
                return None
        '''
        
        result = TinyML_Utils.debounce(self.inference_tuples, time_diff, 
                                       TinyML.__Config_.MIN_INF_TUPLES, 
                                       TinyML.__Config_.TIME_DIFF)
        
        if result is not None:
            print("Debounce result:", result)
            self.inference_tuples = [] # cleans inference tuple buffer after inference
            self.buffer = [] # clears main sensor data buffer after inference
            print("Both buffers cleared after gesture detection")
        
        self.inference_tuples = TinyML_Utils.clean_inf_tuples(self.inference_tuples, time_diff,
                                                         TinyML.__Config_.CLEAN_MAX_TUPLES, 
                                                         TinyML.__Config_.CLEAN_MAX_TIME_DIFF)
        
        return result