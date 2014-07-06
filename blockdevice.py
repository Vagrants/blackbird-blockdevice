#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Low level descovery of block device.
"""

import subprocess

#from blackbird.plugins import base
import base


class ConcreteJob(base.JobBase):

    def __init__(self, options, queue=None, logger=None):
        super(ConcreteJob, self).__init__(options, queue, logger)

    def _enqueue(self, item):
        self.queue.put(item, block=False)
        self.logger.debug(
            'Inserted to queue {key}, {value}'
            ''.format(
                key=item.key,
                value=item.value
            )
        )

    def _get_blockdevice_list(self):
        """
        get block device list by `lsblk` command.
        """
        block_device_list = list()

        cmd = [
            self.options['lsblk_path'],
            '--raw'
        ]
        result = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate(
            subprocess.PIPE
        )

        for line in result[0].split('\n'):
            elements = line.split()

            if (
                len(elements) > 1 and
                elements[self.options['type_column_position']] ==
                self.options['device_type']
            ):
                block_device_list.append(elements[0])

        return block_device_list

    def build_discovery_items(self):
        """
        Low level discovery loop.
        """
        device_list = self._get_blockdevice_list()

        if len(device_list):
            lld_item = base.DiscoveryItem(
                key='vfs.dev.LLD',
                value=[
                    {'{#BLK_DEV}': entry} for entry in device_list
                ],
                host=self.options['hostname']
            )
            self._enqueue(lld_item)


class Validator(base.ValidatorBase):
    """
    This class store information
    which is used by validation config file.
    """

    def __init__(self):
        self.__spec = None

    @property
    def spec(self):
        self.__spec = (
            "[{0}]".format(__name__),
            "lsblk_path = string(default=lsblk)",
            "type_column_position = integer(default=5)",
            "device_type = string(default=disk)",
            "hostname = string(default={0})".format(self.detect_hostname())
        )
        return self.__spec


if __name__ == '__main__':
    OPTIONS = {
        'lsblk_path': 'lsblk',
        'type_column_position': 5,
        'device_type': 'disk',
    }
    JOB = ConcreteJob(
        options=OPTIONS
    )
    print(JOB._get_blockdevice_list())
