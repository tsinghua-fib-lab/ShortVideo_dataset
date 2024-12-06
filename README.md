## Short-video dataset

The full dataset of submission "**A Large-scale Dataset with Behavior, Attributes, and Content of Mobile Short-video Platform**".

#### Main files

- **raw\_file:** the folder containing original video files with the format "video_id.mp4".

- **video\_feature\_total:** the folder containing all extracted visual features with the format "video_id.npy".

- **interaciton.csv:** the file containing all behavior data and attribute data.

- **asr_zn:** ASR text in Chinese of each video with the format "video_id.txt".

- **asr_en:** ASR text in English of each video with the format "video_id.txt".

- **title_en:** Video title in English of each video with the format "video_id.txt".

#### Details of behavior data

| **Field Name** | **Type** | **Description**                                                       | **Example** |
|:---------------------:|:-----------------:|:------------------------------------------------------------------------------:|:--------------------:|
| user\_id              | numeric           | user ID(after hashing), each representing a real user of the platform          | 101                  |
| pid                   | numeric           | video ID(after hashing), each representing a video collected from the platform | 2023                 |
| exposed\_time         | numeric           | Unix timestamp of the interaction                                              | 1663471335           |
| p\_date               | numeric           | date when the interaction happened                                             | 20220917             |
| p\_hour               | numeric           | the hour when the interaction happened                                         | 11                   |
| watch\_time           | numeric           | the given user's watching time towards the given video(seconds)                | 46                   |
| cvm\_like             | bool              | whether the given user gives a like towards the given video                    | True                 |
| comment               | bool              | whether the given user comments for the given video                            | False                |
| follow                | bool              | whether the given user follows the given video                                 | False                |
| collect               | bool              | whether the given user collects the given video                                | True                 |
| forward               | bool              | whether the given user forwards the given video                                | False                |
| effective\_view       | bool              | whether the watching time surpasses 3 seconds                                  | True                 |
| hate                  | bool              | whether the given user gives a hate towards the given video                    | False                |

#### Details of attribute data

##### Video-side attribute data

|  **Field Name**   | **Type** |                       **Description**                        |          **Example**           |
| :---------------: | :------: | :----------------------------------------------------------: | :----------------------------: |
|  category_level   | numeric  | the level of category ID(1: primary category; 2: secondary category; 3: Tertiary category) |               3                |
|    category_id    | numeric  |            the tertiary category ID of the video             |              1350              |
|     parent_id     | numeric  |            the secondary category ID of the video            |              288               |
|      root_id      | numeric  |             the primary category ID of the video             |               39               |
|     duration      | numeric  |             duration of the given video(seconds)             |            138.566             |
|     author_id     | numeric  |           ID of the video’s author(after hashing)            |               78               |
| author_fans_count | numeric  |             number of fans of the video’s author             |             138211             |
|     tag_name      |   text   |                     video’s content tag                      |    ’underwater photography’    |
|       title       |   text   |                      title of the video                      | ’Catch lobsters under the sea’ |

##### User-side attribute data

|   **Field Name**   | **Type** |              **Description**              |    **Example**    |
| :----------------: | :------: | :---------------------------------------: | :---------------: |
|       gender       |   text   | the user’s gender(’M’: male; ’F’: female) |        'M'        |
|        age         | numeric  |              the user’s age               |        34         |
|     mod_price      | numeric  |        the price of user’s phones         |       1899        |
|      fre_city      |   text   |       the city the user locates in        |    'Shanghai'     |
| fre_community_type |   text   |           user’s residence type           |     'country'     |
|   fre_city_level   |   text   |             user’s city level             | 'first-tier city' |
