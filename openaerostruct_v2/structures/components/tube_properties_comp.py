from __future__ import division, print_function
import numpy as np

from openmdao.api import ExplicitComponent


class TubePropertiesComp(ExplicitComponent):

    def initialize(self):
        self.metadata.declare('lifting_surfaces', type_=list)

    def setup(self):
        lifting_surfaces = self.metadata['lifting_surfaces']

        for lifting_surface_name, lifting_surface_data in lifting_surfaces:
            num_points_z = 2 * lifting_surface_data['num_points_z_half'] - 1

            for in_name_ in ['radius', 'thickness']:
                in_name = '{}_tube_{}'.format(lifting_surface_name, in_name_)
                self.add_input(in_name, shape=num_points_z - 1)

            for out_name_ in ['A', 'Iy', 'Iz', 'J']:
                out_name = '{}_element_{}'.format(lifting_surface_name, out_name_)
                self.add_output(out_name, shape=num_points_z - 1)

            arange = np.arange(num_points_z - 1)

            for out_name_ in ['A', 'Iy', 'Iz', 'J']:
                out_name = '{}_element_{}'.format(lifting_surface_name, out_name_)

                for in_name_ in ['radius', 'thickness']:
                    in_name = '{}_tube_{}'.format(lifting_surface_name, in_name_)

                    self.declare_partials(out_name, in_name, rows=arange, cols=arange)

    def compute(self, inputs, outputs):
        lifting_surfaces = self.metadata['lifting_surfaces']

        for lifting_surface_name, lifting_surface_data in lifting_surfaces:
            radius_name = '{}_tube_{}'.format(lifting_surface_name, 'radius')
            thickness_name = '{}_tube_{}'.format(lifting_surface_name, 'thickness')

            A_name = '{}_element_{}'.format(lifting_surface_name, 'A')
            Iy_name = '{}_element_{}'.format(lifting_surface_name, 'Iy')
            Iz_name = '{}_element_{}'.format(lifting_surface_name, 'Iz')
            J_name = '{}_element_{}'.format(lifting_surface_name, 'J')

            r1 = inputs[radius_name] - inputs[thickness_name]
            r2 = inputs[radius_name]

            outputs[A_name] = np.pi * (r2 ** 2 - r1 ** 2)
            outputs[Iy_name] = np.pi * (r2 ** 4 - r1 ** 4) / 4.
            outputs[Iz_name] = np.pi * (r2 ** 4 - r1 ** 4) / 4.
            outputs[J_name] = np.pi * (r2 ** 4 - r1 ** 4) / 2.

    def compute_partials(self, inputs, partials):
        lifting_surfaces = self.metadata['lifting_surfaces']

        dr1_dr = 1.
        dr2_dr = 1.
        dr1_dt = -1.
        dr2_dt =  0.

        for lifting_surface_name, lifting_surface_data in lifting_surfaces:
            radius_name = '{}_tube_{}'.format(lifting_surface_name, 'radius')
            thickness_name = '{}_tube_{}'.format(lifting_surface_name, 'thickness')

            A_name = '{}_element_{}'.format(lifting_surface_name, 'A')
            Iy_name = '{}_element_{}'.format(lifting_surface_name, 'Iy')
            Iz_name = '{}_element_{}'.format(lifting_surface_name, 'Iz')
            J_name = '{}_element_{}'.format(lifting_surface_name, 'J')

            r1 = inputs[radius_name] - inputs[thickness_name]
            r2 = inputs[radius_name]

            partials[A_name, radius_name] = 2 * np.pi * (r2 * dr2_dr - r1 * dr1_dr)
            partials[A_name, thickness_name] = 2 * np.pi * (r2 * dr2_dt - r1 * dr1_dt)
            partials[Iy_name, radius_name] = np.pi * (r2 ** 3 * dr2_dr - r1 ** 3 * dr1_dr)
            partials[Iy_name, thickness_name] = np.pi * (r2 ** 3 * dr2_dt - r1 ** 3 * dr1_dt)
            partials[Iz_name, radius_name] = np.pi * (r2 ** 3 * dr2_dr - r1 ** 3 * dr1_dr)
            partials[Iz_name, thickness_name] = np.pi * (r2 ** 3 * dr2_dt - r1 ** 3 * dr1_dt)
            partials[J_name, radius_name] = 2 * np.pi * (r2 ** 3 * dr2_dr - r1 ** 3 * dr1_dr)
            partials[J_name, thickness_name] = 2 * np.pi * (r2 ** 3 * dr2_dt - r1 ** 3 * dr1_dt)