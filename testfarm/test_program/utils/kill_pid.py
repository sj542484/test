import os,re


class killPid:
    def kill_pid(self, port, node_pid):
        pids = self.get_pid(port=port)
        for i in pids:
            cmd = 'kill -9 {}'.format(i)
            os.popen(cmd)
            print('kill掉 node', cmd)
        cmd = 'kill -9 {}'.format(int(node_pid))
        os.popen(cmd)
        print('kill掉 node',cmd)
        # cmd = 'kill -9 {}'.format(int(node_pid)-1)
        # os.popen(cmd)
        # print('kill掉 node', cmd)

    def get_pid(self, port):
        res = os.popen('lsof -i:%s'%port).read()
        pid = re.findall('.*?node.*?(\d+)', res)
        return set(pid)
