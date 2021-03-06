# ファイル名：sample_sm.py

import rclpy
from rclpy.node import Node
import smach


# 探索の状態を定義します．
class Search(smach.State):
    def __init__(self, _node):
        smach.State.__init__(self, outcomes=['succeeded', 'finished'])
        self.counter = 0
        self.logger = _node.get_logger()

    def execute(self, userdata):
        self.logger.info('探索中です')
        if self.counter < 3:
            self.logger.info('スイーツを見つけました！')
            self.counter += 1
            return 'succeeded'
        else:
            self.logger.info('お腹いっぱいです・・・')
            return 'finished'


# 食事の状態を定義します．
class Eat(smach.State):
    def __init__(self, _node):
        smach.State.__init__(self, outcomes=['done'])
        self.logger = _node.get_logger()

    def execute(self, userdata):
        self.logger.info('食べてます！')
        return 'done'


# ステートマシーンを実行するノードを定義します．
class StateMachine(Node):
    def __init__(self):
        super().__init__('state_machine')

    def execute(self):
        # Smachステートマシーンを作成
        sm = smach.StateMachine(outcomes=['end'])
        # Open the container
        with sm:
            # コンテナに状態を追加
            smach.StateMachine.add(
                'SEARCH', Search(self),
                transitions={'succeeded': 'EAT', 'finished': 'end'})
            smach.StateMachine.add(
                'EAT', Eat(self),
                transitions={'done': 'SEARCH'})

        # Smachプランを実行
        outcome = sm.execute()
        self.get_logger().info(f'outcom: {outcome}')


def main():
    rclpy.init()
    node = StateMachine()
    node.execute()
